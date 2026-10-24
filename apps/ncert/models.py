from django.db import models

from apps.content.models import Subject

BANK_CHOICES = [
    ('mcq', 'Practice MCQ'),
    ('pyq', 'Previous Year Question'),
]

DIFFICULTY_CHOICES = [
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]


class Topic(models.Model):
    """NCERT syllabus topic under one of the 12 content subjects — the
    Subject/Topic dropdown pair in the legacy ncert-module.html prototype's
    hardcoded `databaseMap`, moved into real rows so staff can edit the
    taxonomy from platform_admin instead of a deploy."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='ncert_topics')
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        unique_together = [('subject', 'name')]

    def __str__(self):
        return f'{self.subject.name} / {self.name}'


class Question(models.Model):
    """NCERT-based question bank, scoped to a Topic rather than the
    free-text subject/topic apps.prelims.Question uses — NCERT content
    follows the fixed 12-subject curriculum tree, so a real FK is correct
    here from day one."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    bank = models.CharField(max_length=10, choices=BANK_CHOICES, default='mcq')
    year = models.CharField(max_length=40, blank=True, help_text='e.g. "UPSC 2022" or "NCERT Practice"')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True)
    est_time = models.CharField(max_length=20, blank=True)
    text = models.TextField()
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.topic} — #{self.pk}'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:60]
