from django import forms

from .models import Evaluation, Submission

MAX_IMAGE_SIZE_MB = 5


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['answer_text', 'answer_image']
        widgets = {
            'answer_text': forms.Textarea(attrs={'rows': 10, 'class': 'answer-textarea', 'placeholder': 'Write your answer here.'}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('answer_text') and not cleaned.get('answer_image'):
            raise forms.ValidationError('Write an answer or upload a photo of one.')
        return cleaned

    def clean_answer_image(self):
        image = self.cleaned_data.get('answer_image')
        if image and image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f'Image must be under {MAX_IMAGE_SIZE_MB}MB.')
        return image


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['content_score', 'structure_score', 'examples_score', 'language_score', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'notes-area', 'placeholder': 'Notes (optional)'}),
        }
