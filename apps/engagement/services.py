from django.db import transaction
from django.db.models import F

from .models import Attempt, TopicStat


@transaction.atomic
def record_attempt(user, question, is_correct):
    """Single write path for logging a question attempt — called from
    apps.prelims.views.submit_answer so the counter update and the history
    row never drift apart."""
    Attempt.objects.create(user=user, question=question, is_correct=is_correct)

    stat, _ = TopicStat.objects.get_or_create(
        user=user, subject=question.subject, topic=question.topic,
    )
    stat.total = F('total') + 1
    if is_correct:
        stat.correct = F('correct') + 1
    stat.save(update_fields=['total', 'correct'] if is_correct else ['total'])
