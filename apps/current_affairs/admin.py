from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'source', 'published_date']
    list_filter = ['source', 'category']
    search_fields = ['title', 'summary']
