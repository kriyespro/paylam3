from django.conf import settings
from django.core.cache import cache

from apps.content.models import Subject


def footer_subjects(request):
    """Feeds the footer's subject links on every single page render —
    cached, since subjects change rarely (admin-edited) but this query
    would otherwise run on every request site-wide, including anonymous
    traffic and error pages."""
    subjects = cache.get('footer_subjects')
    if subjects is None:
        subjects = list(Subject.objects.only('slug', 'name').order_by('order', 'name'))
        cache.set('footer_subjects', subjects, 300)
    return {'footer_subjects': subjects}


def google_oauth(request):
    """Lets login/signup templates render the "Sign in with Google" button
    only when a client ID is actually configured (empty in dev by default)."""
    return {'google_client_id': settings.GOOGLE_OAUTH_CLIENT_ID}
