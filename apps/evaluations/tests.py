import io
import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.mains.models import MainsQuestion

from .models import Evaluation, Submission

User = get_user_model()


def make_image_file(name='test.png', width=10, height=10):
    from PIL import Image
    buf = io.BytesIO()
    Image.new('RGB', (width, height), color='red').save(buf, format='PNG')
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type='image/png')


def make_oversized_image_file(name='big.png'):
    """A genuinely incompressible >5MB PNG — a small solid-color image
    compresses to a few KB and wouldn't actually exercise the size check."""
    from PIL import Image
    buf = io.BytesIO()
    width = height = 1600
    noise = os.urandom(width * height * 3)
    Image.frombytes('RGB', (width, height), noise).save(buf, format='PNG')
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type='image/png')


class SubmissionFormTests(TestCase):
    def setUp(self):
        self.question = MainsQuestion.objects.create(external_id='1', paper='GS1', year=2023, marks=10, text='Q?')
        self.user = User.objects.create_user(username='u@example.com', email='u@example.com', password='testpass123')
        self.client.force_login(self.user)
        self.url = reverse('evaluations:submit', kwargs={'question_id': self.question.pk})

    def test_empty_submission_rejected(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Write an answer or upload a photo')
        self.assertEqual(Submission.objects.count(), 0)

    def test_text_only_submission_succeeds(self):
        response = self.client.post(self.url, {'answer_text': 'My answer.'})
        self.assertEqual(Submission.objects.count(), 1)
        submission = Submission.objects.first()
        self.assertRedirects(response, reverse('evaluations:evaluate', kwargs={'pk': submission.pk}))

    def test_oversized_image_rejected(self):
        response = self.client.post(self.url, {'answer_image': make_oversized_image_file()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'must be under')
        self.assertEqual(Submission.objects.count(), 0)

    def test_non_image_file_rejected(self):
        fake = SimpleUploadedFile('fake.jpg', b'this is not an image', content_type='image/jpeg')
        response = self.client.post(self.url, {'answer_image': fake})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Submission.objects.count(), 0)

    def test_anonymous_cannot_submit(self):
        self.client.logout()
        response = self.client.post(self.url, {'answer_text': 'x'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Submission.objects.count(), 0)


class OwnershipTests(TestCase):
    """IDOR checks — a submission id alone must never be enough to see or
    rate someone else's answer."""

    def setUp(self):
        self.question = MainsQuestion.objects.create(external_id='1', paper='GS1', year=2023, marks=10, text='Q?')
        self.owner = User.objects.create_user(username='owner@example.com', email='owner@example.com', password='testpass123')
        self.intruder = User.objects.create_user(username='intruder@example.com', email='intruder@example.com', password='testpass123')
        self.submission = Submission.objects.create(user=self.owner, question=self.question, answer_text='Owner answer')

    def test_other_user_cannot_view_submission_detail(self):
        self.client.force_login(self.intruder)
        response = self.client.get(reverse('evaluations:detail', kwargs={'pk': self.submission.pk}))
        self.assertEqual(response.status_code, 404)

    def test_other_user_cannot_rate_submission(self):
        self.client.force_login(self.intruder)
        url = reverse('evaluations:evaluate', kwargs={'pk': self.submission.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(url, {
            'content_score': 5, 'structure_score': 5, 'examples_score': 5, 'language_score': 5,
        })
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Evaluation.objects.filter(submission=self.submission).exists())

    def test_owner_can_view_and_rate_own_submission(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse('evaluations:detail', kwargs={'pk': self.submission.pk}))
        self.assertEqual(response.status_code, 200)

        url = reverse('evaluations:evaluate', kwargs={'pk': self.submission.pk})
        response = self.client.post(url, {
            'content_score': 5, 'structure_score': 4, 'examples_score': 3, 'language_score': 2,
        })
        self.assertRedirects(response, reverse('evaluations:detail', kwargs={'pk': self.submission.pk}))
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.evaluation.total_score, 14)
