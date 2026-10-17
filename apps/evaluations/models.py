from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.mains.models import MainsQuestion

STAR_VALIDATORS = [MinValueValidator(1), MaxValueValidator(5)]


class Submission(models.Model):
    """A user's answer to a MainsQuestion — text and/or a photo of a
    handwritten answer. Replaces the legacy evaluate.html flow, which never
    persisted anything server-side."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mains_submissions')
    question = models.ForeignKey(MainsQuestion, on_delete=models.CASCADE, related_name='submissions')
    answer_text = models.TextField(blank=True)
    answer_image = models.ImageField(upload_to='evaluations/%Y/%m/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} / {self.question}'


class Evaluation(models.Model):
    """
    Self-rating only, by decision — matches the legacy app's own scope
    (star ratings, self-assessed, never a reviewer or AI in the loop).

    Uses a flat 1-5 scale per criterion rather than the legacy's fixed
    6/4/3/2-point weights: those weights assumed every question is worth 15
    marks, but the imported data has 10-mark questions too (see each
    MainsQuestion.model_answer['scoreHints'] for the real per-question
    breakdown) — copying a rubric that only fits some questions isn't
    "preserving existing behavior," it's preserving an existing bug.
    """
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='evaluation')
    content_score = models.PositiveSmallIntegerField(validators=STAR_VALIDATORS)
    structure_score = models.PositiveSmallIntegerField(validators=STAR_VALIDATORS)
    examples_score = models.PositiveSmallIntegerField(validators=STAR_VALIDATORS)
    language_score = models.PositiveSmallIntegerField(validators=STAR_VALIDATORS)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_score(self):
        return self.content_score + self.structure_score + self.examples_score + self.language_score

    def __str__(self):
        return f'{self.submission} — {self.total_score}/20'
