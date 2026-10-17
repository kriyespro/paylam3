from datetime import date

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import DailyMainsQuestion, MainsQuestion


def question_list(request):
    questions = MainsQuestion.objects.all()

    paper = request.GET.get('paper', '')
    subject = request.GET.get('subject', '')
    year = request.GET.get('year', '')

    if paper:
        questions = questions.filter(paper=paper)
    if subject:
        questions = questions.filter(subject=subject)
    if year:
        questions = questions.filter(year=year)

    paginator = Paginator(questions, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'questions': page_obj,
        'page_obj': page_obj,
        'papers': MainsQuestion.objects.values_list('paper', flat=True).distinct().order_by('paper'),
        'subjects': MainsQuestion.objects.values_list('subject', flat=True).distinct().order_by('subject'),
        'years': MainsQuestion.objects.values_list('year', flat=True).distinct().order_by('-year'),
        'selected_paper': paper,
        'selected_subject': subject,
        'selected_year': year,
    }

    template = 'partials/mains/question_results.html' if request.htmx else 'pages/mains/list.html'
    return render(request, template, context)


def question_practice(request, pk):
    question = get_object_or_404(MainsQuestion, pk=pk)
    return render(request, 'pages/mains/practice.html', {'question': question})


def daily_question(request):
    today = date.today()
    daily = DailyMainsQuestion.objects.filter(date=today).select_related('question').first()

    if not daily:
        question = MainsQuestion.objects.order_by('?').first()
        if question:
            daily = DailyMainsQuestion.objects.create(date=today, question=question)

    return render(request, 'pages/mains/daily.html', {'daily': daily})
