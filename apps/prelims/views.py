from datetime import date

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.engagement.models import Bookmark
from apps.engagement.services import record_attempt

from .models import DailyQuestion, Question


def question_list(request):
    # No prefetch_related('choices') here — the list template never
    # touches choices (only type/subject/difficulty/text), so it was
    # fetching every choice for every matching question on each page
    # load and never using any of it.
    questions = Question.objects.all()

    q_type = request.GET.get('type', '')
    subject = request.GET.get('subject', '')
    difficulty = request.GET.get('difficulty', '')

    if q_type:
        questions = questions.filter(type=q_type)
    if subject:
        questions = questions.filter(subject=subject)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)

    paginator = Paginator(questions, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    bookmarked_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(Bookmark.objects.filter(user=request.user).values_list('question_id', flat=True))

    context = {
        'questions': page_obj,
        'page_obj': page_obj,
        'subjects': Question.objects.values_list('subject', flat=True).distinct().order_by('subject'),
        'difficulties': Question.objects.values_list('difficulty', flat=True).distinct().order_by('difficulty'),
        'selected_type': q_type,
        'selected_subject': subject,
        'selected_difficulty': difficulty,
        'bookmarked_ids': bookmarked_ids,
    }

    template = 'partials/prelims/question_results.html' if request.htmx else 'pages/prelims/list.html'
    return render(request, template, context)


def _next_question(question):
    """Next question of the same type, by pk — wraps to the first once the
    bank runs out so practice never dead-ends."""
    return (
        Question.objects.filter(type=question.type, pk__gt=question.pk).order_by('pk').first()
        or Question.objects.filter(type=question.type).order_by('pk').exclude(pk=question.pk).first()
    )


def question_practice(request, pk):
    question = get_object_or_404(Question.objects.prefetch_related('choices'), pk=pk)
    is_bookmarked = (
        request.user.is_authenticated
        and Bookmark.objects.filter(user=request.user, question=question).exists()
    )
    return render(request, 'pages/prelims/practice.html', {'question': question, 'is_bookmarked': is_bookmarked})


@require_POST
def submit_answer(request, pk):
    question = get_object_or_404(Question.objects.prefetch_related('choices'), pk=pk)
    choice_id = request.POST.get('choice', '')

    # Filter the prefetched list in Python instead of question.choices
    # .filter(...) — calling .filter() on a prefetched related manager
    # bypasses the prefetch cache and re-hits the DB, so the two lookups
    # below used to cost 2 extra queries each request for nothing.
    choices = list(question.choices.all())
    selected = next((c for c in choices if choice_id.isdigit() and c.pk == int(choice_id)), None)

    # Never trust correctness from the client — recompute from the DB row.
    is_correct = bool(selected and selected.is_correct)
    correct_choice = next((c for c in choices if c.is_correct), None)

    if request.user.is_authenticated:
        record_attempt(request.user, question, is_correct)
        if is_correct:
            profile = request.user.profile
            profile.xp += 10
            profile.coins += 5
            profile.save(update_fields=['xp', 'coins'])

    return render(request, 'partials/prelims/answer_result.html', {
        'question': question,
        'selected': selected,
        'is_correct': is_correct,
        'correct_choice': correct_choice,
        'next_question': _next_question(question),
    })


def daily_question(request):
    today = date.today()
    daily = DailyQuestion.objects.filter(date=today).select_related('question').first()

    if not daily:
        question = Question.objects.order_by('?').first()
        if question:
            daily = DailyQuestion.objects.create(date=today, question=question)

    return render(request, 'pages/prelims/daily.html', {'daily': daily})
