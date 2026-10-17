from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import SOURCE_CHOICES, Article


def article_list(request):
    articles = Article.objects.all()

    source = request.GET.get('source', '')
    category = request.GET.get('category', '')

    if source:
        articles = articles.filter(source=source)
    if category:
        articles = articles.filter(category=category)

    paginator = Paginator(articles, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'articles': page_obj,
        'page_obj': page_obj,
        'sources': SOURCE_CHOICES,
        'categories': Article.objects.values_list('category', flat=True).distinct().order_by('category'),
        'selected_source': source,
        'selected_category': category,
    }

    template = 'partials/current_affairs/article_results.html' if request.htmx else 'pages/current_affairs/list.html'
    return render(request, template, context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'pages/current_affairs/detail.html', {'article': article})
