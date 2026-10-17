from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    """A purchasable access tier. Seeded once via the 0002 data migration
    (Starter/Pro/Premium) — editable afterwards from /sd/ without a
    deploy."""

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    price_inr = models.PositiveIntegerField(help_text='Price in rupees (whole, no paise).')
    duration_days = models.PositiveSmallIntegerField(help_text='Access length granted on purchase.')
    features = models.JSONField(default=list, blank=True, help_text='List of feature strings shown on the pricing card.')
    is_popular = models.BooleanField(default=False, help_text='Shows the "Most Popular" badge.')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def price_paise(self):
        """Razorpay's order API takes amounts in the smallest currency
        unit — paise, not rupees."""
        return self.price_inr * 100


class Subscription(models.Model):
    """One purchase attempt. Created in 'created' state the moment a
    Razorpay order is opened, before the user has paid anything — this
    row is what the signature-verified callback and the webhook both look
    up by razorpay_order_id to flip to 'paid'. A user can accumulate many
    rows (retried/abandoned checkouts); the active plan is whichever
    'paid' row has the latest expires_at.
    """

    STATUS_CREATED = 'created'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_CREATED, 'Created'),
        (STATUS_PAID, 'Paid'),
        (STATUS_FAILED, 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')

    razorpay_order_id = models.CharField(max_length=64, unique=True)
    razorpay_payment_id = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED)

    starts_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — {self.plan} ({self.status})'

    def activate(self):
        """Idempotent on purpose — both the browser callback and the
        server-to-server webhook can call this for the same payment, and
        only the first one should actually extend the expiry."""
        if self.status == self.STATUS_PAID:
            return
        now = timezone.now()
        self.status = self.STATUS_PAID
        self.starts_at = now
        self.expires_at = now + timedelta(days=self.plan.duration_days)
        self.save(update_fields=['status', 'starts_at', 'expires_at'])
