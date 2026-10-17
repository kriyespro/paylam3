from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    paginator = Paginator(Post.objects.all(), 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'pages/blog/list.html', {'posts': page_obj, 'page_obj': page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'pages/blog/detail.html', {'post': post})
