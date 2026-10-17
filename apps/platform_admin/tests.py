from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.current_affairs.models import Article
from apps.prelims.models import Choice, Question

User = get_user_model()


class AccessControlTests(TestCase):
    """The actual bug this app was built to fix: a flat redirect sent
    every /admin/ visitor to the same place regardless of who they were.
    These lock in that superusers, staff, regular users, and anonymous
    visitors each land somewhere different and correct."""

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='super@example.com', email='super@example.com', password='testpass123')
        self.staff = User.objects.create_user(username='staff@example.com', email='staff@example.com', password='testpass123', is_staff=True)
        self.regular = User.objects.create_user(username='reg@example.com', email='reg@example.com', password='testpass123')

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse('platform_admin:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_regular_user_redirected_to_own_dashboard(self):
        # Not assertRedirects: dashboard itself 302s onward for an
        # incomplete profile (this test user never ran profile setup),
        # so this only checks platform_admin's own redirect target.
        self.client.force_login(self.regular)
        response = self.client.get(reverse('platform_admin:home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:dashboard'))

    def test_superuser_sees_real_dashboard(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('platform_admin:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content Dashboard')

    def test_staff_sees_real_dashboard(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('platform_admin:home'))
        self.assertEqual(response.status_code, 200)

    def test_regular_user_blocked_from_every_subpage_not_just_home(self):
        self.client.force_login(self.regular)
        for name in ['article_list', 'article_create', 'user_list', 'question_list', 'mains_question_list']:
            response = self.client.get(reverse(f'platform_admin:{name}'))
            self.assertEqual(response.status_code, 302, f'{name} was not gated')
            self.assertEqual(response.url, reverse('accounts:dashboard'), f'{name} redirected to the wrong place')


class ArticleCrudTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username='staff2@example.com', email='staff2@example.com', password='testpass123', is_staff=True)
        self.client.force_login(self.staff)

    def test_create_edit_delete_article(self):
        create_url = reverse('platform_admin:article_create')
        response = self.client.post(create_url, {
            'title': 'Test Article', 'summary': 'Test summary.', 'category': 'Test',
            'source': 'pib', 'icon': 'fas fa-flag', 'published_date': '2026-01-01',
        })
        self.assertRedirects(response, reverse('platform_admin:article_list'))
        article = Article.objects.get(title='Test Article')

        edit_url = reverse('platform_admin:article_update', kwargs={'pk': article.pk})
        response = self.client.post(edit_url, {
            'title': 'Test Article Edited', 'summary': 'Test summary.', 'category': 'Test',
            'source': 'pib', 'icon': 'fas fa-flag', 'published_date': '2026-01-01',
        })
        self.assertRedirects(response, reverse('platform_admin:article_list'))
        article.refresh_from_db()
        self.assertEqual(article.title, 'Test Article Edited')

        delete_url = reverse('platform_admin:article_delete', kwargs={'pk': article.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('platform_admin:article_list'))
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())


class QuestionFormsetTests(TestCase):
    """The inline Choice formset is the trickiest form in this app —
    covers create with a marked-correct choice, and that the correctness
    flag actually lands on the right row."""

    def setUp(self):
        self.staff = User.objects.create_user(username='staff3@example.com', email='staff3@example.com', password='testpass123', is_staff=True)
        self.client.force_login(self.staff)

    def test_create_question_with_choices(self):
        response = self.client.post(reverse('platform_admin:question_create'), {
            'external_id': 'FORMSET_TEST', 'type': 'mcq', 'year': 'Mock Test', 'subject': 'Test',
            'topic': 'Test', 'difficulty': 'Easy', 'est_time': '30s',
            'text': 'Test question?', 'explanation': 'Because.',
            'choices-TOTAL_FORMS': '2', 'choices-INITIAL_FORMS': '0',
            'choices-MIN_NUM_FORMS': '2', 'choices-MAX_NUM_FORMS': '1000',
            'choices-0-text': 'Right', 'choices-0-is_correct': 'on', 'choices-0-order': '0',
            'choices-1-text': 'Wrong', 'choices-1-order': '1',
        })
        self.assertRedirects(response, reverse('platform_admin:question_list'))

        question = Question.objects.get(external_id='FORMSET_TEST')
        self.assertEqual(question.choices.count(), 2)
        correct = question.choices.get(is_correct=True)
        self.assertEqual(correct.text, 'Right')

    def test_invalid_json_on_mains_question_does_not_crash(self):
        """Same failure class as the choice-id bug from Phase 6 — bad input
        should fail the form, not 500."""
        from apps.mains.models import MainsQuestion
        mq = MainsQuestion.objects.create(external_id='JSON_TEST', paper='GS1', year=2023, marks=10, text='Q?')
        response = self.client.post(reverse('platform_admin:mains_question_update', kwargs={'pk': mq.pk}), {
            'external_id': 'JSON_TEST', 'paper': 'GS1', 'year': '2023', 'subject': 'Test', 'marks': '10',
            'text': 'Q?', 'model_answer_json': '{not valid json',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid JSON')


class BackupRestoreTests(TestCase):
    """Backup is staff-readable (non-destructive); restore is genuinely
    destructive (upserts by PK over live data), so it's gated stricter —
    superuser only, not just staff. These lock in that distinction, since
    it's the actual security boundary of this feature."""

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='super@example.com', email='super@example.com', password='testpass123')
        self.staff = User.objects.create_user(username='staff@example.com', email='staff@example.com', password='testpass123', is_staff=True)
        self.regular = User.objects.create_user(username='reg@example.com', email='reg@example.com', password='testpass123')
        Article.objects.create(title='Test Article', summary='S', category='C', source='pib', published_date='2026-01-01')

    def test_staff_can_download_backup(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('platform_admin:backup_download'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/gzip')

    def test_regular_user_cannot_download_backup(self):
        self.client.force_login(self.regular)
        response = self.client.get(reverse('platform_admin:backup_download'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:dashboard'))

    def test_superuser_can_access_restore(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('platform_admin:restore_upload'))
        self.assertEqual(response.status_code, 200)

    def test_staff_non_superuser_cannot_access_restore(self):
        """The actual point of SuperuserRequiredMixin — plain is_staff
        must not be enough for this one view."""
        self.client.force_login(self.staff)
        response = self.client.get(reverse('platform_admin:restore_upload'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('platform_admin:home'))

    def test_backup_then_restore_round_trip_preserves_data(self):
        """The actual feature working end to end, not just access-gated:
        download a real backup, wipe the article, restore, confirm it's
        back with the exact same content."""
        import gzip

        self.client.force_login(self.superuser)
        backup_response = self.client.get(reverse('platform_admin:backup_download'))
        backup_bytes = b''.join(backup_response.streaming_content) if backup_response.streaming else backup_response.content

        Article.objects.all().delete()
        self.assertEqual(Article.objects.count(), 0)

        from django.core.files.uploadedfile import SimpleUploadedFile
        upload = SimpleUploadedFile('backup.json.gz', backup_bytes, content_type='application/gzip')
        response = self.client.post(reverse('platform_admin:restore_upload'), {
            'confirm_phrase': 'RESTORE',
            'backup_file': upload,
        })
        self.assertRedirects(response, reverse('platform_admin:home'))

        restored = Article.objects.get(title='Test Article')
        self.assertEqual(restored.summary, 'S')

    def test_wrong_confirm_phrase_does_nothing(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse('platform_admin:restore_upload'), {
            'confirm_phrase': 'restore',  # lowercase — must not match
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Type RESTORE exactly')
        self.assertEqual(Article.objects.count(), 1)  # untouched

    def test_garbage_file_fails_safely_without_touching_data(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.client.force_login(self.superuser)
        upload = SimpleUploadedFile('garbage.json', b'not a real backup', content_type='application/json')
        response = self.client.post(reverse('platform_admin:restore_upload'), {
            'confirm_phrase': 'RESTORE',
            'backup_file': upload,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restore failed')
        self.assertEqual(Article.objects.count(), 1)  # untouched, not partially applied


class AnalyticsTests(TestCase):
    """Not revenue — this app has no payments anywhere. Real activity
    counts (signups/attempts/submissions) from data already in the DB."""

    def setUp(self):
        self.staff = User.objects.create_user(username='staff4@example.com', email='staff4@example.com', password='testpass123', is_staff=True)
        self.regular = User.objects.create_user(username='reg2@example.com', email='reg2@example.com', password='testpass123')

    def test_staff_can_view_analytics(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('platform_admin:analytics'))
        self.assertEqual(response.status_code, 200)

    def test_regular_user_blocked(self):
        self.client.force_login(self.regular)
        response = self.client.get(reverse('platform_admin:analytics'))
        self.assertEqual(response.status_code, 302)

    def test_signup_total_matches_real_signups_in_window(self):
        """response.context is None for Jinja2-rendered responses in this
        Django version (confirmed, not assumed — the first version of this
        test tried response.context['signups_total'] and got a TypeError),
        so this asserts against a dedicated data-testid marker in the
        template rather than scraping an ambiguous bare number from HTML.
        self.regular is the only non-staff signup in this test's DB —
        self.staff is excluded (is_staff=True)."""
        self.client.force_login(self.staff)
        response = self.client.get(reverse('platform_admin:analytics'))
        self.assertContains(response, 'data-testid="signups-total">1<')
