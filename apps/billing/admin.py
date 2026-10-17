from django.contrib import admin

from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price_inr', 'duration_days', 'is_popular', 'order']
    list_editable = ['order', 'is_popular']
    ordering = ['order']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'razorpay_order_id', 'starts_at', 'expires_at', 'created_at']
    list_filter = ['status', 'plan']
    search_fields = ['user__username', 'user__email', 'razorpay_order_id', 'razorpay_payment_id']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'created_at']
