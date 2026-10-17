from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SignupTests(TestCase):
    def test_signup_creates_user_and_profile(self):
        response = self.client.post(reverse('accounts:signup'), {
            'full_name': 'Test Student',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'target_exam': 'UPSC',
        })
        self.assertRedirects(response, reverse('accounts:profile_setup'))
        user = User.objects.get(username='newuser@example.com')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.display_name, 'Test Student')

    def test_duplicate_email_rejected(self):
        User.objects.create_user(username='dup@example.com', email='dup@example.com', password='x')
        response = self.client.post(reverse('accounts:signup'), {
            'full_name': 'Another',
            'email': 'dup@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)  # re-renders form, no redirect
        self.assertContains(response, 'already exists')

    def test_weak_password_rejected(self):
        response = self.client.post(reverse('accounts:signup'), {
            'full_name': 'Weak Pw',
            'email': 'weak@example.com',
            'password': 'short',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='weak@example.com').exists())


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='login@example.com', email='login@example.com', password='correctpass123')

    def test_correct_credentials_succeed(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'login@example.com',
            'password': 'correctpass123',
        })
        # Not assertRedirects: dashboard itself 302s onward for an
        # incomplete profile (covered in DashboardAccessTests), so this
        # only checks that login itself redirects to dashboard, not what
        # dashboard does next.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:dashboard'))

    def test_wrong_password_fails(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'login@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_nonexistent_email_fails(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'nobody@example.com',
            'password': 'whatever123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reset@example.com', email='reset@example.com', password='oldpass123')

    def test_full_reset_flow_changes_password(self):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        response = self.client.post(reverse('accounts:password_reset'), {'email': 'reset@example.com'})
        self.assertRedirects(response, reverse('accounts:password_reset_done'))

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        confirm_url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        session_response = self.client.get(confirm_url, follow=True)
        set_password_url = session_response.redirect_chain[-1][0]

        response = self.client.post(set_password_url, {
            'new_password1': 'brandnewpass456',
            'new_password2': 'brandnewpass456',
        })
        self.assertRedirects(response, reverse('accounts:password_reset_complete'))

        self.client.logout()
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'reset@example.com',
            'password': 'brandnewpass456',
        })
        self.assertEqual(login_response.status_code, 302)
        self.assertEqual(login_response.url, reverse('accounts:dashboard'))


class DashboardAccessTests(TestCase):
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_incomplete_profile_redirected_to_setup(self):
        user = User.objects.create_user(username='incomplete@example.com', email='incomplete@example.com', password='testpass123')
        self.client.force_login(user)
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertRedirects(response, reverse('accounts:profile_setup'))
