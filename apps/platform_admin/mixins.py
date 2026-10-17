from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


class StaffRequiredMixin(UserPassesTestMixin):
    """Gates every platform_admin view to staff/superusers ('Superadmin and
    Website Owner') — anonymous users go to the real login page, logged-in
    non-staff users go to their own dashboard rather than a bare 403, since
    landing here at all means they followed a link meant for someone else,
    not that they did anything wrong."""

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), login_url='accounts:login')
        return redirect('accounts:dashboard')


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Stricter than StaffRequiredMixin — for the one view in this app that
    can actually overwrite live data (restore-from-backup). Regular staff
    can still get bounced to /admin/, they just can't reach this one."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), login_url='accounts:login')
        return redirect('platform_admin:home')
