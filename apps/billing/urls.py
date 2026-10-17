from django.urls import path

from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.plan_list, name='plans'),
    path('checkout/<slug:slug>/', views.checkout, name='checkout'),
    path('verify/', views.verify_payment, name='verify'),
    path('webhook/', views.razorpay_webhook, name='webhook'),
    path('success/', views.payment_success, name='success'),
    path('failed/', views.payment_failed, name='failed'),
]
