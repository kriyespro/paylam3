import json

from django import forms

from apps.blog.models import Post
from apps.content.models import Subject
from apps.current_affairs.models import Article
from apps.mains.models import MainsQuestion
from apps.prelims.models import Choice, Question

ADMIN_INPUT_ATTRS = {'class': 'pa-input'}
ADMIN_TEXTAREA_ATTRS = {'class': 'pa-input', 'rows': 5}


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'category', 'source', 'icon', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'summary': forms.Textarea(attrs=ADMIN_TEXTAREA_ATTRS),
            'category': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'icon': forms.TextInput(attrs={**ADMIN_INPUT_ATTRS, 'placeholder': 'fas fa-leaf'}),
            'published_date': forms.DateInput(attrs={**ADMIN_INPUT_ATTRS, 'type': 'date'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'slug': forms.TextInput(attrs={**ADMIN_INPUT_ATTRS, 'placeholder': 'auto-filled from title if left blank'}),
            'body': forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 12}),
            'published_date': forms.DateInput(attrs={**ADMIN_INPUT_ATTRS, 'type': 'date'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'icon', 'theme', 'tagline', 'order']
        widgets = {
            'name': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'icon': forms.TextInput(attrs={**ADMIN_INPUT_ATTRS, 'placeholder': 'fas fa-landmark'}),
            'theme': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'tagline': forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 2}),
            'order': forms.NumberInput(attrs=ADMIN_INPUT_ATTRS),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['external_id', 'type', 'year', 'subject', 'topic', 'difficulty', 'est_time', 'text', 'explanation']
        widgets = {
            'external_id': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'type': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'year': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'subject': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'topic': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'difficulty': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'est_time': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'text': forms.Textarea(attrs=ADMIN_TEXTAREA_ATTRS),
            'explanation': forms.Textarea(attrs=ADMIN_TEXTAREA_ATTRS),
        }


ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice,
    fields=['text', 'is_correct', 'order'],
    extra=1, can_delete=True, min_num=2, validate_min=True,
    widgets={
        'text': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
        'order': forms.NumberInput(attrs={**ADMIN_INPUT_ATTRS, 'style': 'width:70px;'}),
    },
)


class MainsQuestionForm(forms.ModelForm):
    model_answer_json = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 14, 'style': 'font-family:monospace;font-size:0.85rem;'}),
        required=False,
        label='Model Answer (JSON)',
        help_text='Keys: intro, forPoints[{head,body}], againstPoints[{head,body}], wayForward[{label,desc}], conclusion, scoreHints[], tags[]. Leave blank for no model answer yet.',
    )

    class Meta:
        model = MainsQuestion
        fields = ['external_id', 'paper', 'year', 'subject', 'marks', 'text']
        widgets = {
            'external_id': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'paper': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'year': forms.NumberInput(attrs=ADMIN_INPUT_ATTRS),
            'subject': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'marks': forms.NumberInput(attrs=ADMIN_INPUT_ATTRS),
            'text': forms.Textarea(attrs=ADMIN_TEXTAREA_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['model_answer_json'].initial = json.dumps(self.instance.model_answer, indent=2, ensure_ascii=False)

    def clean_model_answer_json(self):
        raw = self.cleaned_data.get('model_answer_json', '').strip()
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError(f'Invalid JSON: {exc}')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.model_answer = self.cleaned_data.get('model_answer_json', {})
        if commit:
            instance.save()
        return instance
