from django.http import HttpResponse
from django.shortcuts import render

from apps.content.models import Subject
from apps.engagement.models import Attempt
from apps.evaluations.models import Submission
from apps.mains.views import get_todays_daily as get_todays_daily_mains
from apps.prelims.views import get_todays_daily as get_todays_daily_prelims


def home(request):
    daily_prelims = get_todays_daily_prelims()
    daily_mains = get_todays_daily_mains()
    context = {
        'subjects': Subject.objects.all(),
        'daily_prelims': daily_prelims,
        'daily_prelims_attempts': Attempt.objects.filter(question=daily_prelims.question).count() if daily_prelims else 0,
        'daily_mains': daily_mains,
        'daily_mains_attempts': Submission.objects.filter(question=daily_mains.question).count() if daily_mains else 0,
    }
    return render(request, 'pages/home.html', context)


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
