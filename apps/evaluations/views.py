import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.mains.models import MainsQuestion

from .forms import EvaluationForm, SubmissionForm
from .models import Submission

logger = logging.getLogger(__name__)


@login_required
def my_evaluations(request):
    submissions = Submission.objects.filter(user=request.user).select_related('question', 'evaluation')
    return render(request, 'pages/evaluations/list.html', {'submissions': submissions})


@login_required
def submission_create(request, question_id):
    question = get_object_or_404(MainsQuestion, pk=question_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.question = question
            submission.save()
            logger.info('Submission %s created by user %s for question %s', submission.pk, request.user, question.pk)
            return redirect('evaluations:evaluate', pk=submission.pk)
    else:
        form = SubmissionForm()

    return render(request, 'pages/evaluations/submit.html', {'form': form, 'question': question})


@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(
        Submission.objects.select_related('question', 'evaluation'),
        pk=pk, user=request.user,
    )
    return render(request, 'pages/evaluations/detail.html', {'submission': submission})


@login_required
def evaluation_create(request, pk):
    # Scoped to request.user — a submission id alone is never enough to
    # rate (or see) someone else's answer.
    submission = get_object_or_404(Submission.objects.select_related('question'), pk=pk, user=request.user)

    existing = getattr(submission, 'evaluation', None)

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=existing)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.submission = submission
            evaluation.save()
            logger.info('Evaluation saved for submission %s (score %s/20)', submission.pk, evaluation.total_score)
            return redirect('evaluations:detail', pk=submission.pk)
    else:
        form = EvaluationForm(instance=existing)

    return render(request, 'pages/evaluations/evaluate.html', {'form': form, 'submission': submission})
