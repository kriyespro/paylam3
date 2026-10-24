from django.contrib import admin

from .models import Choice, Question, Topic


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'order']
    list_filter = ['subject']
    ordering = ['subject', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'bank', 'difficulty', 'year']
    list_filter = ['bank', 'difficulty', 'topic__subject']
    inlines = [ChoiceInline]
