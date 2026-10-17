from django.shortcuts import get_object_or_404, render

from .models import Subject


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'pages/content/subject_list.html', {'subjects': subjects})


def subject_detail(request, slug):
    subject = get_object_or_404(
        Subject.objects.prefetch_related('modules__units__lessons'),
        slug=slug,
    )
    return render(request, 'pages/content/subject_detail.html', {'subject': subject})
