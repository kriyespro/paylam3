from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.prelims.models import Question

from .models import Attempt, Bookmark, TopicStat
from .services import record_attempt

User = get_user_model()


class BookmarkToggleTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(external_id='Q1', type='mcq', text='Q?')
        self.user = User.objects.create_user(username='u@example.com', email='u@example.com', password='testpass123')

    def test_toggle_creates_then_removes_bookmark(self):
        self.client.force_login(self.user)
        url = reverse('engagement:toggle_bookmark', kwargs={'pk': self.question.pk})

        self.client.post(url)
        self.assertTrue(Bookmark.objects.filter(user=self.user, question=self.question).exists())

        self.client.post(url)
        self.assertFalse(Bookmark.objects.filter(user=self.user, question=self.question).exists())

    def test_anonymous_cannot_toggle(self):
        url = reverse('engagement:toggle_bookmark', kwargs={'pk': self.question.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bookmark.objects.count(), 0)


class RecordAttemptTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(external_id='Q1', type='mcq', subject='Polity', topic='Rights', text='Q?')
        self.user = User.objects.create_user(username='u@example.com', email='u@example.com', password='testpass123')

    def test_creates_attempt_and_topic_stat(self):
        record_attempt(self.user, self.question, True)
        record_attempt(self.user, self.question, False)

        self.assertEqual(Attempt.objects.filter(user=self.user).count(), 2)
        stat = TopicStat.objects.get(user=self.user, subject='Polity', topic='Rights')
        self.assertEqual(stat.total, 2)
        self.assertEqual(stat.correct, 1)
