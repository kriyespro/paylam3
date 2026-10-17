from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile, SUBJECT_CHOICES

User = get_user_model()


class SignupForm(forms.Form):
    """
    No custom User model (see models.py docstring) — email doubles as the
    username. Django allows '@' in usernames, so no custom auth backend
    is needed to log in by email later.
    """
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Your full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Min 8 characters'}), min_length=8)
    target_exam = forms.CharField(
        max_length=100, required=False, initial='UPSC',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. UPSC'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self):
        email = self.cleaned_data['email']
        full_name = self.cleaned_data['full_name'].strip()
        user = User.objects.create_user(
            username=email,
            email=email,
            password=self.cleaned_data['password'],
            first_name=full_name.split(' ')[0],
        )
        profile = user.profile
        profile.display_name = full_name
        profile.target_exam = self.cleaned_data.get('target_exam') or 'UPSC'
        profile.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    password = forms.CharField(
        label='Password', strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),
    )

    def clean_username(self):
        return self.cleaned_data['username'].strip().lower()


STUDY_HOURS_CHOICES = [(1, '1 hour / day'), (2, '2 hours / day'), (3, '3 hours / day'), (4, '4 hours / day'), (6, '6 hours / day'), (8, '8 hours / day'), (10, '10+ hours / day')]
DAILY_Q_CHOICES = [(10, '10 questions / day'), (20, '20 questions / day'), (30, '30 questions / day'), (50, '50 questions / day'), (100, '100 questions / day')]


class ProfileSetupForm(forms.ModelForm):
    study_goal_hours = forms.TypedChoiceField(choices=STUDY_HOURS_CHOICES, coerce=int, required=False, initial=4)
    daily_q_target = forms.TypedChoiceField(choices=DAILY_Q_CHOICES, coerce=int, required=False, initial=30)
    subjects = forms.MultipleChoiceField(
        choices=[(s, s) for s in SUBJECT_CHOICES],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'display_name', 'study_goal_hours', 'daily_q_target', 'exam_date', 'subjects']
        widgets = {
            'avatar': forms.HiddenInput(),
            'display_name': forms.TextInput(attrs={'placeholder': 'What should we call you?', 'maxlength': 30}),
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.profile_complete = True
        if commit:
            profile.save()
        return profile
