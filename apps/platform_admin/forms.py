import json
import re

from django import forms
from django.utils.safestring import mark_safe

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


_SECTION_HEADERS = {
    'in favor': 'forPoints', 'points in favor': 'forPoints', 'for': 'forPoints',
    'pros': 'forPoints', 'favor': 'forPoints', 'favour': 'forPoints', 'in favour': 'forPoints',
    'against': 'againstPoints', 'points against': 'againstPoints', 'cons': 'againstPoints',
    'limitations': 'againstPoints', 'against / limitations': 'againstPoints',
    'way forward': 'wayForward', 'wayforward': 'wayForward',
    'conclusion': 'conclusion',
    'tags': 'tags',
    'scoring guide': 'scoreHints', 'score hints': 'scoreHints', 'scorehints': 'scoreHints', 'hints': 'scoreHints',
}

_BULLET_RE = re.compile(r'^(?:[-*•]|\d+[.)])\s*')


def _strip_bullet(line):
    return _BULLET_RE.sub('', line.strip()).strip()


def _detect_header(line):
    """Recognize a section header line, with or without a trailing colon,
    and with or without content after it on the same line (e.g. both
    'Tags:' alone and 'Tags: governance, polity' are headers)."""
    whole = line.rstrip(':').strip().lower()
    if whole in _SECTION_HEADERS:
        return _SECTION_HEADERS[whole], ''
    head, sep, rest = line.partition(':')
    if sep:
        key = head.strip().lower()
        if key in _SECTION_HEADERS:
            return _SECTION_HEADERS[key], rest.strip()
    return None, None


def parse_plain_model_answer(text):
    """Turn a freely-typed answer (plain paragraphs + optional section
    headers like 'In Favor:', 'Way Forward:', 'Tags:') into the model_answer
    JSON shape, so a non-technical admin never has to write JSON or any
    special delimiter syntax."""
    section = 'intro'
    buckets = {'intro': [], 'forPoints': [], 'againstPoints': [], 'wayForward': [], 'conclusion': [], 'tags': [], 'scoreHints': []}
    for raw_line in (text or '').splitlines():
        line = raw_line.strip()
        if not line:
            continue
        header, inline = _detect_header(line)
        if header:
            section = header
            if inline:
                buckets[section].append(inline)
            continue
        buckets[section].append(line)

    model_answer = {}
    if buckets['intro']:
        model_answer['intro'] = ' '.join(buckets['intro'])

    for key, part_names in (('forPoints', ('head', 'body')), ('againstPoints', ('head', 'body'))):
        pairs = []
        for line in buckets[key]:
            line = _strip_bullet(line)
            head, sep, body = line.partition(':')
            pairs.append({part_names[0]: head.strip() if sep else '', part_names[1]: (body if sep else head).strip()})
        if pairs:
            model_answer[key] = pairs

    way_forward = []
    for line in buckets['wayForward']:
        line = _strip_bullet(line)
        label, sep, desc = line.partition(':')
        way_forward.append({'label': label.strip() if sep else '', 'desc': (desc if sep else label).strip()})
    if way_forward:
        model_answer['wayForward'] = way_forward

    if buckets['conclusion']:
        model_answer['conclusion'] = ' '.join(buckets['conclusion'])

    score_hints = [_strip_bullet(line) for line in buckets['scoreHints']]
    if score_hints:
        model_answer['scoreHints'] = score_hints

    tags = [t.strip() for line in buckets['tags'] for t in line.split(',') if t.strip()]
    if tags:
        model_answer['tags'] = tags

    return model_answer


def render_plain_model_answer(model_answer):
    """Reverse of parse_plain_model_answer, so editing an existing question
    shows the same friendly plain text instead of raw JSON."""
    model_answer = model_answer or {}
    lines = []
    if model_answer.get('intro'):
        lines.append(model_answer['intro'])

    def _pairs_block(header, items, part_names):
        if not items:
            return
        lines.append('')
        lines.append(f'{header}:')
        for item in items:
            head = item.get(part_names[0], '')
            body = item.get(part_names[1], '')
            lines.append(f'- {head}: {body}' if head else f'- {body}')

    _pairs_block('In Favor', model_answer.get('forPoints'), ('head', 'body'))
    _pairs_block('Against', model_answer.get('againstPoints'), ('head', 'body'))
    _pairs_block('Way Forward', model_answer.get('wayForward'), ('label', 'desc'))

    if model_answer.get('conclusion'):
        lines.append('')
        lines.append('Conclusion:')
        lines.append(model_answer['conclusion'])

    if model_answer.get('scoreHints'):
        lines.append('')
        lines.append('Scoring Guide:')
        for hint in model_answer['scoreHints']:
            lines.append(f'- {hint}')

    if model_answer.get('tags'):
        lines.append('')
        lines.append('Tags: ' + ', '.join(model_answer['tags']))

    return '\n'.join(lines)


MODEL_ANSWER_JSON_TEMPLATE = """{
  "intro": "Opening paragraph introducing the issue.",
  "forPoints": [
    {"head": "Short heading", "body": "Explanation of this point."}
  ],
  "againstPoints": [
    {"head": "Short heading", "body": "Explanation of this point."}
  ],
  "wayForward": [
    {"label": "Step label", "desc": "What this step involves."}
  ],
  "conclusion": "Closing paragraph.",
  "scoreHints": [
    "Mention a real example or case study.",
    "Use a diagram or flowchart where relevant."
  ],
  "tags": ["governance", "polity"]
}"""

MODEL_ANSWER_AI_PROMPT = """Convert the answer below into JSON that follows this exact template (same keys, same structure, fill in the content, remove any sections that don't apply):

""" + MODEL_ANSWER_JSON_TEMPLATE + """

ANSWER TO CONVERT:
<paste your plain-text model answer here>"""

ANSWER_TEXT_HELP = mark_safe(
    "Paste your answer as plain text — no JSON, no special formatting needed. It's saved as-is.<br><br>"
    "Want it to show up in sections (In Favor / Against / Way Forward / Conclusion) on the student "
    "page? Start those parts with one of these lines on its own: <code>In Favor:</code>, "
    "<code>Against:</code>, <code>Way Forward:</code>, <code>Conclusion:</code>, <code>Tags:</code>, "
    "<code>Scoring Guide:</code> — then list each point on its own line. Everything before the first "
    "such line is the introduction. This is entirely optional; a plain answer with no headers is saved "
    "as the introduction and works fine.<br><br>"
    '<strong>Example:</strong>'
    '<pre style="white-space:pre-wrap;background:#1118;padding:8px;border-radius:6px;">'
    'Right to Information Act empowers citizens to seek information from public authorities.\n\n'
    'In Favor:\n'
    '- Transparency: Opens up government decision-making to public scrutiny.\n'
    '- Accountability: Makes officials answerable for delays and decisions.\n\n'
    'Against:\n'
    '- Misuse: Can be used to harass officials with frivolous queries.\n\n'
    'Way Forward:\n'
    '- Digitisation: Move RTI filing and replies fully online.\n\n'
    'Conclusion:\n'
    'RTI remains a vital tool for participatory democracy despite implementation gaps.\n\n'
    'Tags: governance, polity'
    '</pre>'
)

MODEL_ANSWER_JSON_HELP = mark_safe(
    '<strong>Advanced, optional.</strong> Paste ready-made JSON here instead — if this box has '
    'anything in it, the plain-text answer above is ignored.<br><br>'
    '<strong>Template:</strong>'
    f'<pre style="white-space:pre-wrap;background:#1118;padding:8px;border-radius:6px;">{MODEL_ANSWER_JSON_TEMPLATE}</pre>'
    '<strong>Don’t want to write JSON by hand?</strong> Copy this prompt into ChatGPT/Claude '
    'along with your plain-text answer, and paste what it gives back into this box:'
    f'<pre style="white-space:pre-wrap;background:#1118;padding:8px;border-radius:6px;">{MODEL_ANSWER_AI_PROMPT}</pre>'
)


class MainsQuestionForm(forms.ModelForm):
    answer_text = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 12}),
        required=False,
        label='Model Answer',
        help_text=ANSWER_TEXT_HELP,
    )
    model_answer_json = forms.CharField(
        widget=forms.Textarea(attrs={**ADMIN_TEXTAREA_ATTRS, 'rows': 10, 'style': 'font-family:monospace;font-size:0.85rem;'}),
        required=False,
        label='Model Answer: Paste JSON (advanced, optional)',
        help_text=MODEL_ANSWER_JSON_HELP,
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
        self.fields['answer_text'].initial = render_plain_model_answer(answer)

    def clean_model_answer_json(self):
        raw = self.cleaned_data.get('model_answer_json', '').strip()
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError(f'Invalid JSON: {exc}')
        if not isinstance(parsed, dict):
            raise forms.ValidationError('JSON must be an object (e.g. {"intro": "...", ...}), not a list or plain value.')
        return parsed

    def save(self, commit=True):
        instance = super().save(commit=False)
        data = self.cleaned_data
        if data.get('model_answer_json'):
            instance.model_answer = data['model_answer_json']
        else:
            instance.model_answer = parse_plain_model_answer(data.get('answer_text', ''))
        if commit:
            instance.save()
        return instance
