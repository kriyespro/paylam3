from django.db import models

QUESTION_TYPE_CHOICES = [
    ('pyq', 'Previous Year Question'),
    ('mcq', 'Practice MCQ'),
]

DIFFICULTY_CHOICES = [
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]


class Question(models.Model):
    """
    Ported from api.js's MockDB — pyqBank/mcqBank arrays hardcoded in JS and
    shipped to every client. `external_id` keeps the legacy id (e.g.
    "PYQ_2022_POL_04") so re-running the import stays idempotent.

    `subject`/`topic` are free-text here, not FKs to apps.content.Subject —
    the legacy strings ("Indian Polity") don't line up 1:1 with content
    app's slugs, and forcing that join now would be guessing. Worth doing
    once both models are stable, not before.
    """
    external_id = models.CharField(max_length=60, unique=True)
    type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    year = models.CharField(max_length=40, blank=True, help_text='e.g. "UPSC 2022" or "Mock Test"')
    subject = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=150, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True)
    est_time = models.CharField(max_length=20, blank=True)
    text = models.TextField(help_text='Question body — legacy data embeds inline <br>/<strong> HTML')
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.external_id


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:60]


class DailyQuestion(models.Model):
    """One featured Question per calendar date. The legacy version wasn't
    actually daily — MockDB seeded a single hardcoded question once, ever,
    into localStorage, and it never rotated. `views.daily_question` picks a
    new one automatically when today has no row yet, which is a genuine
    improvement over that, not a behavior change anyone relied on."""
    date = models.DateField(unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='daily_picks')
    xp = models.PositiveIntegerField(default=50)
    coins = models.PositiveIntegerField(default=20)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.date}: {self.question.external_id}'
