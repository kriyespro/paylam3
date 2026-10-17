from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Question

User = get_user_model()


class SubmitAnswerTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            external_id='TEST_Q1', type='mcq', subject='Test Subject', topic='Test Topic', text='2+2=?',
        )
        self.correct = Choice.objects.create(question=self.question, text='4', is_correct=True, order=0)
        self.wrong = Choice.objects.create(question=self.question, text='5', is_correct=False, order=1)

        self.other_question = Question.objects.create(external_id='TEST_Q2', type='mcq', text='Other?')
        self.other_choice = Choice.objects.create(question=self.other_question, text='X', is_correct=True)

        self.user = User.objects.create_user(username='u@example.com', email='u@example.com', password='testpass123')

    def test_correct_answer_awards_xp_and_coins(self):
        self.client.force_login(self.user)
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'choice': self.correct.pk})
        self.assertContains(response, 'Correct!')
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.xp, 10)
        self.assertEqual(self.user.profile.coins, 5)

    def test_wrong_answer_does_not_award_xp(self):
        self.client.force_login(self.user)
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'choice': self.wrong.pk})
        self.assertContains(response, 'Not quite')
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.xp, 0)

    def test_bogus_choice_id_is_safe_not_correct(self):
        self.client.force_login(self.user)
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'choice': 999999})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Not quite')

    def test_choice_from_different_question_is_not_credited(self):
        """A choice id that's real but belongs to a different question must
        never be treated as correct just because is_correct=True on that
        other question — the lookup has to be scoped to this question."""
        self.client.force_login(self.user)
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'choice': self.other_choice.pk})
        self.assertContains(response, 'Not quite')
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.xp, 0)

    def test_empty_choice_does_not_crash(self):
        self.client.force_login(self.user)
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'choice': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Not quite')

    def test_non_numeric_choice_does_not_crash(self):
        self.client.force_login(self.user)
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'choice': 'not-a-number'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Not quite')

    def test_anonymous_submission_does_not_crash_or_award(self):
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'choice': self.correct.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Correct!')

    def test_repeat_correct_submission_awards_again(self):
        """No submit-once guard — documents the actual (accepted) behavior
        rather than assuming one exists."""
        self.client.force_login(self.user)
        url = reverse('prelims:submit_answer', kwargs={'pk': self.question.pk})
        self.client.post(url, {'choice': self.correct.pk})
        self.client.post(url, {'choice': self.correct.pk})
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.xp, 20)


class FilterTests(TestCase):
    def setUp(self):
        Question.objects.create(external_id='A', type='pyq', subject='Polity', text='Q1')
        Question.objects.create(external_id='B', type='mcq', subject='History', text='Q2')

    def test_subject_filter_narrows_results(self):
        response = self.client.get(reverse('prelims:list'), {'subject': 'Polity'})
        self.assertContains(response, 'Q1')
        self.assertNotContains(response, 'Q2')

    def test_htmx_request_returns_partial_not_full_page(self):
        full = self.client.get(reverse('prelims:list'))
        partial = self.client.get(reverse('prelims:list'), HTTP_HX_REQUEST='true')
        self.assertContains(full, '<nav')
        self.assertNotContains(partial, '<nav')
