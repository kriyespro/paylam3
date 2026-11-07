from django.contrib import admin

from apps.platform_admin.forms import MainsQuestionForm

from .models import DailyMainsQuestion, MainsQuestion


@admin.register(MainsQuestion)
class MainsQuestionAdmin(admin.ModelAdmin):
    form = MainsQuestionForm
    list_display = ['external_id', 'paper', 'year', 'subject', 'marks']
    list_filter = ['paper', 'year', 'subject']
    search_fields = ['external_id', 'text']


@admin.register(DailyMainsQuestion)
class DailyMainsQuestionAdmin(admin.ModelAdmin):
    list_display = ['date', 'question']
