from django.db import models

PAPER_CHOICES = [
    ('Essay', 'Essay'),
    ('GS1', 'GS1'),
    ('GS2', 'GS2'),
    ('GS3', 'GS3'),
    ('GS4', 'GS4'),
]


class MainsQuestion(models.Model):
    """
    Ported from mains-pyq-data.js's mainsPYQData array. `model_answer` keeps
    the legacy structure as-is (intro/forPoints/againstPoints/wayForward/
    conclusion/scoreHints/tags) — it's genuinely rich structured content,
    not worth flattening into separate columns nothing queries by.

    No submission/scoring model here on purpose: the legacy UI only ever
    self-rated answers client-side (star ratings, never persisted anywhere).
    Real submission + scoring is apps.evaluations' job (Phase 6), and that
    phase's scoring method (self-rate/manual/AI) is still an open decision —
    building a MainsSession model here with nothing to persist yet would be
    a stub with no behavior, not a real feature.
    """
    external_id = models.CharField(max_length=20, unique=True)
    paper = models.CharField(max_length=10, choices=PAPER_CHOICES)
    year = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=100, blank=True)
    marks = models.PositiveSmallIntegerField()
    text = models.TextField()
    model_answer = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'paper']

    def __str__(self):
        return f'{self.paper} {self.year} #{self.external_id}'


class DailyMainsQuestion(models.Model):
    """Same pattern as apps.prelims.DailyQuestion — one featured question
    per date, auto-picked by the view when today has no row yet."""
    date = models.DateField(unique=True)
    question = models.ForeignKey(MainsQuestion, on_delete=models.CASCADE, related_name='daily_picks')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.date}: {self.question.external_id}'
