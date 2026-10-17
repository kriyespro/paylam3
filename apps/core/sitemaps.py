from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Post
from apps.content.models import Subject
from apps.current_affairs.models import Article


class SubjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Subject.objects.all()

    def location(self, obj):
        return reverse('content:detail', kwargs={'slug': obj.slug})


class ArticleSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.published_date

    def location(self, obj):
        return reverse('current_affairs:detail', kwargs={'pk': obj.pk})


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.published_date

    def location(self, obj):
        return reverse('blog:detail', kwargs={'slug': obj.slug})


class StaticViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['core:home', 'content:list', 'prelims:list', 'mains:list', 'current_affairs:list', 'blog:list']

    def location(self, item):
        return reverse(item)
