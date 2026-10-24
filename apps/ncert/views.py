from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.content.models import Subject

from .models import Question, Topic


def question_list(request):
    questions = Question.objects.select_related('topic', 'topic__subject')

    subject_slug = request.GET.get('subject', '')
    topic_id = request.GET.get('topic', '')
    bank = request.GET.get('bank', '')

    if subject_slug:
        questions = questions.filter(topic__subject__slug=subject_slug)
    if topic_id:
        questions = questions.filter(topic_id=topic_id)
    if bank:
        questions = questions.filter(bank=bank)

    paginator = Paginator(questions, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    topics = Topic.objects.filter(subject__slug=subject_slug) if subject_slug else Topic.objects.none()

    context = {
        'questions': page_obj,
        'page_obj': page_obj,
        'subjects': Subject.objects.all(),
        'topics': topics,
        'selected_subject': subject_slug,
        'selected_topic': topic_id,
        'selected_bank': bank,
    }
    template = 'partials/ncert/question_results.html' if request.htmx else 'pages/ncert/list.html'
    return render(request, template, context)


def topic_options(request):
    """HTMX partial — repopulates the Topic <select> when Subject changes."""
    subject_slug = request.GET.get('subject', '')
    topics = Topic.objects.filter(subject__slug=subject_slug) if subject_slug else Topic.objects.none()
    return render(request, 'partials/ncert/topic_options.html', {'topics': topics})


def _next_question(question):
    """Next question in the same topic, by pk — wraps to the first once the
    bank runs out so practice never dead-ends."""
    return (
        Question.objects.filter(topic=question.topic, pk__gt=question.pk).order_by('pk').first()
        or Question.objects.filter(topic=question.topic).order_by('pk').exclude(pk=question.pk).first()
    )


def question_practice(request, pk):
    question = get_object_or_404(
        Question.objects.prefetch_related('choices').select_related('topic', 'topic__subject'), pk=pk,
    )
    return render(request, 'pages/ncert/practice.html', {'question': question})


@require_POST
def submit_answer(request, pk):
    question = get_object_or_404(Question.objects.prefetch_related('choices'), pk=pk)
    choice_id = request.POST.get('choice', '')

    choices = list(question.choices.all())
    selected = next((c for c in choices if choice_id.isdigit() and c.pk == int(choice_id)), None)

    # Never trust correctness from the client — recompute from the DB row.
    is_correct = bool(selected and selected.is_correct)
    correct_choice = next((c for c in choices if c.is_correct), None)

    if request.user.is_authenticated and is_correct:
        profile = request.user.profile
        profile.xp += 10
        profile.coins += 5
        profile.save(update_fields=['xp', 'coins'])

    return render(request, 'partials/ncert/answer_result.html', {
        'question': question,
        'selected': selected,
        'is_correct': is_correct,
        'correct_choice': correct_choice,
        'next_question': _next_question(question),
    })
