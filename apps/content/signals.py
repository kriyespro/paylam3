from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Subject


@receiver([post_save, post_delete], sender=Subject)
def clear_footer_subjects_cache(sender, **kwargs):
    """The footer_subjects context processor caches this for 5 minutes —
    invalidate immediately on edit so admin changes (via /admin/ or /sd/)
    show up right away instead of waiting out the TTL."""
    cache.delete('footer_subjects')
