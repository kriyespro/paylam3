from django.contrib import admin

from .models import Evaluation, Submission


class EvaluationInline(admin.StackedInline):
    model = Evaluation
    extra = 0


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    list_filter = ['user']
    inlines = [EvaluationInline]
