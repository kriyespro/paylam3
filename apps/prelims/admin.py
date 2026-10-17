from django.contrib import admin

from .models import Choice, DailyQuestion, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'type', 'subject', 'topic', 'difficulty', 'year']
    list_filter = ['type', 'subject', 'difficulty']
    search_fields = ['external_id', 'text', 'topic']
    inlines = [ChoiceInline]


@admin.register(DailyQuestion)
class DailyQuestionAdmin(admin.ModelAdmin):
    list_display = ['date', 'question', 'xp', 'coins']
