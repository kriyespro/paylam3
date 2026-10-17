from django.conf import settings
from django.db import models

from apps.prelims.models import Question


class Bookmark(models.Model):
    """Replaces storage.js's toggleBookmark/getBookmarks/isBookmarked,
    which kept a plain array of question ids in localStorage."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'question')]
        ordering = ['-created_at']


class Attempt(models.Model):
    """Replaces storage.js's logAttempt. Anonymous submissions never reach
    here — apps.prelims.views.submit_answer only calls record_attempt for
    an authenticated user, same gate it already uses for XP/coins."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class TopicStat(models.Model):
    """Replaces storage.js's updateTopicStats/getTopicStats. Keyed on the
    same free-text subject/topic strings Question already uses (see
    apps.prelims.models.Question docstring on why those aren't FKs yet)."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_stats')
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=150, blank=True)
    total = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [('user', 'subject', 'topic')]

    def __str__(self):
        return f'{self.user}: {self.subject}/{self.topic} ({self.correct}/{self.total})'
