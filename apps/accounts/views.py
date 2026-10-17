import logging
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from apps.engagement.models import Attempt, Bookmark, TopicStat

from .forms import EmailAuthenticationForm, ProfileSetupForm, SignupForm

logger = logging.getLogger(__name__)
User = get_user_model()


class EmailLoginView(LoginView):
    template_name = 'pages/accounts/login.html'
    authentication_form = EmailAuthenticationForm

    def form_invalid(self, form):
        logger.warning('Failed login attempt for username=%r', self.request.POST.get('username', ''))
        return super().form_invalid(form)


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicit backend required now that axes adds a second one to
            # AUTHENTICATION_BACKENDS — login() can't infer which backend
            # "authenticated" a user that was just created directly rather
            # than via authenticate(). ModelBackend is correct here: the
            # user just proved their identity by completing signup, axes'
            # failure-tracking applies to actual login attempts, not this.
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:profile_setup')
    else:
        form = SignupForm()

    return render(request, 'pages/accounts/signup.html', {'form': form})


@csrf_exempt
@require_POST
def google_login(request):
    """Handles Google Identity Services' "login_uri" button flow: GSI
    POSTs here directly (no page JS involved), carrying the signed
    credential plus a `g_csrf_token` double-submitted as both a cookie and
    a form field. Django's own CSRF middleware can't validate this POST —
    there's no Django csrf token in it — so this view is exempt and
    instead checks Google's double-submit cookie itself, per Google's
    documented login_uri contract.
    """
    cookie_token = request.COOKIES.get('g_csrf_token')
    body_token = request.POST.get('g_csrf_token')
    if not cookie_token or not body_token or cookie_token != body_token:
        return HttpResponseBadRequest('Missing or mismatched g_csrf_token.')

    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        logger.error('Google login attempted but GOOGLE_OAUTH_CLIENT_ID is not configured.')
        messages.error(request, 'Google sign-in is not available right now.')
        return redirect('accounts:login')

    credential = request.POST.get('credential', '')
    try:
        payload = google_id_token.verify_oauth2_token(
            credential, google_requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID,
        )
    except ValueError:
        logger.warning('Invalid Google credential presented at login.')
        messages.error(request, 'Google sign-in failed. Please try again.')
        return redirect('accounts:login')

    email = (payload.get('email') or '').strip().lower()
    if not email or not payload.get('email_verified'):
        messages.error(request, 'Your Google account has no verified email.')
        return redirect('accounts:login')

    full_name = payload.get('name') or email.split('@')[0]
    user, created = User.objects.get_or_create(
        username=email,
        defaults={'email': email, 'first_name': full_name.split(' ')[0]},
    )
    if created:
        # No password — this account only ever logs in via Google.
        user.set_unusable_password()
        user.save(update_fields=['password'])
        profile = user.profile
        profile.display_name = full_name
        profile.save(update_fields=['display_name'])

    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    if not user.profile.profile_complete:
        return redirect('accounts:profile_setup')
    return redirect('accounts:dashboard')


@login_required
def profile_setup(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard')
    else:
        form = ProfileSetupForm(instance=profile)

    return render(request, 'pages/accounts/profile_setup.html', {'form': form})


@login_required
def dashboard(request):
    profile = request.user.profile
    if not profile.profile_complete:
        return redirect('accounts:profile_setup')

    attempts = Attempt.objects.filter(user=request.user)
    totals = attempts.aggregate(total=Count('id'), correct=Count('id', filter=Q(is_correct=True)))
    total_attempts = totals['total']
    avg_score = round(totals['correct'] / total_attempts * 100) if total_attempts else 0

    today_attempts = attempts.filter(created_at__date=date.today()).count()
    daily_target = profile.daily_q_target or 0
    daily_progress_pct = min(100, round(today_attempts / daily_target * 100)) if daily_target else 0

    topic_stats = TopicStat.objects.filter(user=request.user).order_by('-total')[:8]
    subjects_practiced = TopicStat.objects.filter(user=request.user).values('subject').distinct().count()
    bookmarks_count = Bookmark.objects.filter(user=request.user).count()
    recent_attempts = attempts.select_related('question').order_by('-created_at')[:5]

    context = {
        'profile': profile,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'today_attempts': today_attempts,
        'daily_target': daily_target,
        'daily_progress_pct': daily_progress_pct,
        'topic_stats': topic_stats,
        'subjects_practiced': subjects_practiced,
        'bookmarks_count': bookmarks_count,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'pages/accounts/dashboard.html', context)
