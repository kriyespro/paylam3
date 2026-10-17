from django.conf import settings
from django.db import models

SUBJECT_CHOICES = [
    'Polity', 'History', 'Geography', 'Economy', 'Environment',
    'Governance', 'International Relations', 'Internal Security',
    'Disaster Management', 'Ethics', 'Social Issue', 'Science & Tech',
]


class Profile(models.Model):
    """
    One-to-one companion to django.contrib.auth.User. Holds everything the
    old client-side auth.js kept on the fake tb_current_user object — avatar,
    exam target, onboarding state, and lightweight gamification counters.

    Detailed activity aggregates (questions attempted, per-topic accuracy)
    stay out of this model on purpose — those get computed from
    apps.engagement.Attempt once that app exists (Phase 8), not duplicated
    here as stale counters.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    display_name = models.CharField(max_length=150, blank=True)
    avatar = models.CharField(max_length=8, default='📚')
    target_exam = models.CharField(max_length=100, default='UPSC')
    exam_date = models.DateField(null=True, blank=True)

    profile_complete = models.BooleanField(default=False)
    study_goal_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    daily_q_target = models.PositiveSmallIntegerField(null=True, blank=True)
    subjects = models.JSONField(default=list, blank=True)

    xp = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.user.get_username()

    @property
    def first_name_display(self):
        name = self.display_name or self.user.first_name or self.user.get_username()
        return name.split(' ')[0]
