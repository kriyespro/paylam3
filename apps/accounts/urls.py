from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('google/', views.google_login, name='google_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='pages/accounts/password_reset_form.html',
            email_template_name='pages/accounts/password_reset_email.html',
            subject_template_name='pages/accounts/password_reset_subject.txt',
            success_url=reverse_lazy('accounts:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='pages/accounts/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='pages/accounts/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='pages/accounts/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]
