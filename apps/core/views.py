from django.http import HttpResponse
from django.shortcuts import render

from apps.content.models import Subject


def home(request):
    return render(request, 'pages/home.html', {'subjects': Subject.objects.all()})


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /sd/',
        'Disallow: /admin/',
        'Disallow: /accounts/',
        'Disallow: /evaluations/',
        'Disallow: /bookmarks/',
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
