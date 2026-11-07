from django import forms

from apps.blog.models import Post
from apps.content.models import Subject
from apps.current_affairs.models import Article
from apps.mains.models import MainsQuestion
from apps.ncert.models import Choice as NcertChoice, Question as NcertQuestion, Topic as NcertTopic
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


class NcertTopicForm(forms.ModelForm):
    class Meta:
        model = NcertTopic
        fields = ['subject', 'name', 'order']
        widgets = {
            'subject': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'name': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'order': forms.NumberInput(attrs=ADMIN_INPUT_ATTRS),
        }


class NcertQuestionForm(forms.ModelForm):
    class Meta:
        model = NcertQuestion
        fields = ['topic', 'bank', 'year', 'difficulty', 'est_time', 'text', 'explanation']
        widgets = {
            'topic': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'bank': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'year': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'difficulty': forms.Select(attrs=ADMIN_INPUT_ATTRS),
            'est_time': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
            'text': forms.Textarea(attrs=ADMIN_TEXTAREA_ATTRS),
            'explanation': forms.Textarea(attrs=ADMIN_TEXTAREA_ATTRS),
        }


NcertChoiceFormSet = forms.inlineformset_factory(
    NcertQuestion, NcertChoice,
    fields=['text', 'is_correct', 'order'],
    extra=1, can_delete=True, min_num=2, validate_min=True,
    widgets={
        'text': forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
        'order': forms.NumberInput(attrs={**ADMIN_INPUT_ATTRS, 'style': 'width:70px;'}),
    },
)


def _lines_to_pairs(raw, part_names):
    """Turn 'Head | Body' per-line text into [{part_names[0]: head, part_names[1]: body}, ...]."""
    pairs = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        first, sep, second = line.partition('|')
        pairs.append({part_names[0]: first.strip(), part_names[1]: second.strip() if sep else ''})
    return pairs


def _pairs_to_lines(pairs, part_names):
    return '\n'.join(
        f"{item.get(part_names[0], '')} | {item.get(part_names[1], '')}"
        for item in (pairs or [])
    )


def _lines_to_list(raw):
    return [line.strip() for line in raw.splitlines() if line.strip()]


class MainsQuestionForm(forms.ModelForm):
    intro = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 3}),
        required=False,
        label='Model Answer: Introduction',
        help_text='Opening paragraph of the model answer. Leave blank if not adding a model answer yet.',
    )
    for_points = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 5}),
        required=False,
        label='Model Answer: Points In Favor',
        help_text='One point per line, as Heading | Explanation. Example: Transparency | Opens up decision-making to public scrutiny',
    )
    against_points = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 5}),
        required=False,
        label='Model Answer: Points Against / Limitations',
        help_text='One point per line, as Heading | Explanation.',
    )
    way_forward = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 5}),
        required=False,
        label='Model Answer: Way Forward',
        help_text='One step per line, as Step Label | Description.',
    )
    conclusion = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 3}),
        required=False,
        label='Model Answer: Conclusion',
        help_text='Closing paragraph of the model answer.',
    )
    score_hints = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 3}),
        required=False,
        label='Model Answer: Scoring Guide',
        help_text='One hint per line.',
    )
    tags = forms.CharField(
        widget=forms.TextInput(attrs=ADMIN_INPUT_ATTRS),
        required=False,
        label='Model Answer: Tags',
        help_text='Comma-separated, e.g. governance, polity, ethics',
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
        answer = self.instance.model_answer if self.instance and self.instance.pk else {}
        self.fields['intro'].initial = answer.get('intro', '')
        self.fields['for_points'].initial = _pairs_to_lines(answer.get('forPoints'), ('head', 'body'))
        self.fields['against_points'].initial = _pairs_to_lines(answer.get('againstPoints'), ('head', 'body'))
        self.fields['way_forward'].initial = _pairs_to_lines(answer.get('wayForward'), ('label', 'desc'))
        self.fields['conclusion'].initial = answer.get('conclusion', '')
        self.fields['score_hints'].initial = '\n'.join(answer.get('scoreHints') or [])
        self.fields['tags'].initial = ', '.join(answer.get('tags') or [])

    def save(self, commit=True):
        instance = super().save(commit=False)
        data = self.cleaned_data
        model_answer = {}
        if data.get('intro', '').strip():
            model_answer['intro'] = data['intro'].strip()
        for_points = _lines_to_pairs(data.get('for_points', ''), ('head', 'body'))
        if for_points:
            model_answer['forPoints'] = for_points
        against_points = _lines_to_pairs(data.get('against_points', ''), ('head', 'body'))
        if against_points:
            model_answer['againstPoints'] = against_points
        way_forward = _lines_to_pairs(data.get('way_forward', ''), ('label', 'desc'))
        if way_forward:
            model_answer['wayForward'] = way_forward
        if data.get('conclusion', '').strip():
            model_answer['conclusion'] = data['conclusion'].strip()
        score_hints = _lines_to_list(data.get('score_hints', ''))
        if score_hints:
            model_answer['scoreHints'] = score_hints
        tags = [t.strip() for t in data.get('tags', '').split(',') if t.strip()]
        if tags:
            model_answer['tags'] = tags
        instance.model_answer = model_answer
        if commit:
            instance.save()
        return instance
