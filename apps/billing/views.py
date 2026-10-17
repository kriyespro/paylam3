import hashlib
import hmac
import json
import logging

import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Plan, Subscription

logger = logging.getLogger(__name__)


def _client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def plan_list(request):
    return render(request, 'pages/billing/plans.html', {'plans': Plan.objects.all()})


@login_required
def checkout(request, slug):
    plan = get_object_or_404(Plan, slug=slug)

    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        logger.error('Checkout attempted but Razorpay keys are not configured.')
        return render(request, 'pages/billing/unavailable.html', status=503)

    order = _client().order.create({
        'amount': plan.price_paise,
        'currency': 'INR',
        'notes': {'plan_slug': plan.slug, 'user_id': str(request.user.pk)},
    })

    Subscription.objects.create(user=request.user, plan=plan, razorpay_order_id=order['id'])

    # JSON-encoded, not raw string interpolation: these land inside a
    # <script> block as JS string literals, and json.dumps is what
    # guarantees quotes/backslashes in a name or email can't break out of
    # the literal or inject script.
    context = {
        'plan': plan,
        'amount_paise': plan.price_paise,
        'order_id_json': json.dumps(order['id']),
        'key_id_json': json.dumps(settings.RAZORPAY_KEY_ID),
        'verify_url_json': json.dumps(reverse('billing:verify')),
        'description_json': json.dumps(f'{plan.name} Plan — {plan.duration_days // 30} Months'),
        'user_name_json': json.dumps(request.user.get_full_name() or request.user.get_username()),
        'user_email_json': json.dumps(request.user.email),
    }
    return render(request, 'pages/billing/checkout.html', context)


@login_required
@require_POST
def verify_payment(request):
    """Razorpay Checkout's JS posts here with these three fields once the
    user completes payment in the widget. The signature is what proves
    the payment actually happened — without checking it, anyone could
    POST a fabricated order/payment id pair and get a free subscription.
    """
    order_id = request.POST.get('razorpay_order_id', '')
    payment_id = request.POST.get('razorpay_payment_id', '')
    signature = request.POST.get('razorpay_signature', '')

    subscription = get_object_or_404(Subscription, razorpay_order_id=order_id, user=request.user)

    try:
        _client().utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        })
    except razorpay.errors.SignatureVerificationError:
        logger.warning('Razorpay signature verification failed for order=%s', order_id)
        subscription.status = Subscription.STATUS_FAILED
        subscription.save(update_fields=['status'])
        return redirect('billing:failed')

    subscription.razorpay_payment_id = payment_id
    subscription.activate()
    return redirect('billing:success')


@csrf_exempt
@require_POST
def razorpay_webhook(request):
    """Server-to-server backstop for verify_payment: if the user closes
    the tab right after paying, Checkout's JS callback never fires and
    the subscription would stay stuck at 'created' forever. Razorpay
    POSTs this regardless of what the browser does, so it's the one path
    guaranteed to activate the subscription. Configure the same secret as
    the webhook's signing secret in the Razorpay dashboard.
    """
    secret = settings.RAZORPAY_WEBHOOK_SECRET
    if not secret:
        return HttpResponseBadRequest('Webhook secret not configured.')

    body = request.body
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    signature = request.headers.get('X-Razorpay-Signature', '')
    if not hmac.compare_digest(expected, signature):
        logger.warning('Razorpay webhook signature mismatch.')
        return HttpResponseBadRequest('Invalid signature.')

    payload = json.loads(body)
    if payload.get('event') == 'payment.captured':
        entity = payload['payload']['payment']['entity']
        subscription = Subscription.objects.filter(razorpay_order_id=entity['order_id']).first()
        if subscription:
            subscription.razorpay_payment_id = entity['id']
            subscription.activate()

    return HttpResponse(status=200)


def payment_success(request):
    return render(request, 'pages/billing/success.html')


def payment_failed(request):
    return render(request, 'pages/billing/failed.html')
