from django.contrib import admin

from .models import Attempt, Bookmark, TopicStat


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    list_filter = ['user']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_correct', 'created_at']
    list_filter = ['is_correct', 'user']


@admin.register(TopicStat)
class TopicStatAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'topic', 'total', 'correct']
    list_filter = ['subject']
