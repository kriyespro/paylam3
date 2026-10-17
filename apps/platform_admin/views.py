import gzip
import io
import logging
import os
import tempfile
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import management
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView, View

from apps.blog.models import Post
from apps.content.models import Subject
from apps.current_affairs.models import Article
from apps.engagement.models import Attempt, Bookmark
from apps.evaluations.models import Evaluation, Submission
from apps.mains.models import MainsQuestion
from apps.prelims.models import Question

from .forms import ArticleForm, ChoiceFormSet, MainsQuestionForm, PostForm, QuestionForm, SubjectForm
from .mixins import StaffRequiredMixin, SuperuserRequiredMixin

User = get_user_model()
logger = logging.getLogger(__name__)


class DashboardHome(StaffRequiredMixin, TemplateView):
    template_name = 'pages/platform_admin/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        counts = {
            'subjects': Subject.objects.count(),
            'prelims_questions': Question.objects.count(),
            'mains_questions': MainsQuestion.objects.count(),
            'articles': Article.objects.count(),
            'posts': Post.objects.count(),
            'users': User.objects.filter(is_staff=False).count(),
            'submissions': Submission.objects.count(),
            'evaluations': Evaluation.objects.count(),
        }

        # "Platform Status" chart — 4 categories, each rolling up counts
        # that individually already have their own stat card above.
        status_bars = [
            ('Content', counts['subjects'] + counts['articles'] + counts['posts'], 'fas fa-book-open'),
            ('Question Bank', counts['prelims_questions'] + counts['mains_questions'], 'fas fa-check-square'),
            ('Users', counts['users'], 'fas fa-users'),
            ('Engagement', counts['submissions'] + counts['evaluations'], 'fas fa-chart-line'),
        ]
        max_bar = max((value for _, value, _ in status_bars), default=0) or 1
        platform_status = [
            {'label': label, 'value': value, 'icon': icon, 'pct': round(value / max_bar * 100)}
            for label, value, icon in status_bars
        ]

        ctx.update({
            'active': 'home',
            'counts': counts,
            'platform_status': platform_status,
            'recent_users': User.objects.filter(is_staff=False).order_by('-date_joined')[:6],
            'recent_submissions': Submission.objects.select_related('user', 'question').order_by('-created_at')[:6],
            'attempts_today': Attempt.objects.filter(created_at__date=date.today()).count(),
        })
        return ctx


# ---------- Backup / Restore ----------
# Portable (works identically against SQLite dev or Postgres prod) since
# it's Django's own dumpdata/loaddata rather than a pg_dump binary — no
# extra dependency in the web container, no DB-engine-specific format.

BACKUP_EXCLUDE = [
    'sessions',        # ephemeral, meaningless to restore
    'admin',            # LogEntry — audit trail, not content
    'contenttypes',     # rebuilt automatically by Django on migrate
    'auth.permission',  # rebuilt automatically by Django on migrate
    'axes',             # login-attempt tracking, not content
]


class BackupDownloadView(StaffRequiredMixin, View):
    """Non-destructive, read-only — any staff member can pull a backup.
    Contains user accounts (incl. password hashes) and all real content;
    the file itself is only as safe as wherever the downloading browser
    saves it, same trust level as /sd/ or the rest of this dashboard."""

    def get(self, request):
        buffer = io.StringIO()
        management.call_command(
            'dumpdata',
            exclude=BACKUP_EXCLUDE,
            indent=2,
            stdout=buffer,
        )
        compressed = gzip.compress(buffer.getvalue().encode('utf-8'))
        timestamp = date.today().isoformat()
        logger.info('Backup downloaded by %s', request.user)

        response = HttpResponse(compressed, content_type='application/gzip')
        response['Content-Disposition'] = f'attachment; filename="thebasics-backup-{timestamp}.json.gz"'
        return response


class RestoreUploadView(SuperuserRequiredMixin, View):
    """Superuser-only — this overwrites any row whose primary key already
    exists in the uploaded backup (Django's loaddata semantics: upsert by
    PK, not a full wipe-then-reload). Wrapped in one transaction so a
    failed restore leaves existing data untouched rather than half-applied."""

    def get(self, request):
        return render(request, 'pages/platform_admin/restore.html')

    def post(self, request):
        confirm = request.POST.get('confirm_phrase', '')
        uploaded = request.FILES.get('backup_file')

        if confirm != 'RESTORE':
            messages.error(request, 'Type RESTORE exactly (all caps) to confirm.')
            return render(request, 'pages/platform_admin/restore.html')

        if not uploaded:
            messages.error(request, 'Choose a backup file first.')
            return render(request, 'pages/platform_admin/restore.html')

        try:
            raw = uploaded.read()
            if uploaded.name.endswith('.gz'):
                raw = gzip.decompress(raw)
            text = raw.decode('utf-8')
        except (OSError, UnicodeDecodeError, gzip.BadGzipFile) as exc:
            messages.error(request, f"Couldn't read that file as a backup: {exc}")
            return render(request, 'pages/platform_admin/restore.html')

        # loaddata's `stdin` isn't a real call_command option in this
        # Django version (call_command only special-cases stdout/stderr,
        # not stdin) — passing it raises "Unknown option(s)". Writing to
        # a real temp file and passing that path as the fixture label is
        # loaddata's actual supported interface.
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
                tmp.write(text)
                tmp_path = tmp.name
            with transaction.atomic():
                management.call_command('loaddata', tmp_path, format='json')
        except Exception as exc:
            logger.warning('Restore attempted by %s failed, rolled back: %s', request.user, exc)
            messages.error(request, f'Restore failed — nothing was changed. Error: {exc}')
            return render(request, 'pages/platform_admin/restore.html')
        finally:
            if tmp_path:
                os.unlink(tmp_path)

        logger.info('Restore completed by %s', request.user)
        messages.success(request, 'Restore completed successfully.')
        return redirect('platform_admin:home')


# ---------- Analytics ----------

def _daily_counts(queryset, date_field, days):
    """Real per-day counts for the last N days, zero-filled for days with
    no activity — annotate+values only returns rows that actually have
    data, so without the fill a quiet day would just be missing from the
    series instead of showing as 0, making the chart misleading."""
    today = date.today()
    start = today - timedelta(days=days - 1)
    rows = (
        queryset.filter(**{f'{date_field}__date__gte': start})
        .annotate(day=TruncDate(date_field))
        .values('day')
        .annotate(count=Count('id'))
    )
    counts_by_day = {row['day']: row['count'] for row in rows}
    return [
        {'date': start + timedelta(days=i), 'count': counts_by_day.get(start + timedelta(days=i), 0)}
        for i in range(days)
    ]


class AnalyticsView(StaffRequiredMixin, TemplateView):
    """Real activity trends from data already in the DB — signups,
    question attempts, mains submissions per day. Not revenue: this app
    has no payments/monetization anywhere (see roadmap.md's scope note),
    so "activity" is what's actually being measured here."""
    template_name = 'pages/platform_admin/analytics.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        days = 14

        signups = _daily_counts(User.objects.filter(is_staff=False), 'date_joined', days)
        attempts = _daily_counts(Attempt.objects.all(), 'created_at', days)
        submissions = _daily_counts(Submission.objects.all(), 'created_at', days)

        def with_pct(series):
            max_count = max((d['count'] for d in series), default=0) or 1
            return [{**d, 'pct': round(d['count'] / max_count * 100)} for d in series]

        ctx.update({
            'active': 'analytics',
            'signups': with_pct(signups),
            'attempts': with_pct(attempts),
            'submissions': with_pct(submissions),
            'signups_total': sum(d['count'] for d in signups),
            'attempts_total': sum(d['count'] for d in attempts),
            'submissions_total': sum(d['count'] for d in submissions),
        })
        return ctx


# ---------- Generic CRUD mixins for the simple content types ----------

class AdminListView(StaffRequiredMixin, ListView):
    paginate_by = 25
    template_name = 'pages/platform_admin/generic_list.html'


class AdminCreateView(StaffRequiredMixin, CreateView):
    template_name = 'pages/platform_admin/generic_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} created.')
        return super().form_valid(form)


class AdminUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'pages/platform_admin/generic_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} updated.')
        return super().form_valid(form)


class AdminDeleteView(StaffRequiredMixin, DeleteView):
    template_name = 'pages/platform_admin/generic_confirm_delete.html'

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} deleted.')
        return super().form_valid(form)


# ---------- Articles ----------

class ArticleListView(AdminListView):
    model = Article
    ordering = ['-published_date']
    extra_context = {
        'active': 'articles',
        'title': 'Current Affairs Articles',
        'columns': [('Title', 'title'), ('Category', 'category'), ('Source', 'get_source_display'), ('Published', 'published_date')],
        'create_url': reverse_lazy('platform_admin:article_create'),
        'edit_url_name': 'platform_admin:article_update',
        'delete_url_name': 'platform_admin:article_delete',
    }


class ArticleCreateView(AdminCreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('platform_admin:article_list')
    extra_context = {'active': 'articles', 'title': 'New Article', 'cancel_url': reverse_lazy('platform_admin:article_list')}


class ArticleUpdateView(AdminUpdateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('platform_admin:article_list')
    extra_context = {'active': 'articles', 'title': 'Edit Article', 'cancel_url': reverse_lazy('platform_admin:article_list')}


class ArticleDeleteView(AdminDeleteView):
    model = Article
    success_url = reverse_lazy('platform_admin:article_list')
    extra_context = {'active': 'articles', 'title': 'Delete Article', 'cancel_url': reverse_lazy('platform_admin:article_list')}


# ---------- Blog Posts ----------

class PostListView(AdminListView):
    model = Post
    ordering = ['-published_date']
    extra_context = {
        'active': 'posts',
        'title': 'Blog Posts',
        'columns': [('Title', 'title'), ('Published', 'published_date')],
        'create_url': reverse_lazy('platform_admin:post_create'),
        'edit_url_name': 'platform_admin:post_update',
        'delete_url_name': 'platform_admin:post_delete',
    }


class PostCreateView(AdminCreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('platform_admin:post_list')
    extra_context = {'active': 'posts', 'title': 'New Blog Post', 'cancel_url': reverse_lazy('platform_admin:post_list')}


class PostUpdateView(AdminUpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('platform_admin:post_list')
    extra_context = {'active': 'posts', 'title': 'Edit Blog Post', 'cancel_url': reverse_lazy('platform_admin:post_list')}


class PostDeleteView(AdminDeleteView):
    model = Post
    success_url = reverse_lazy('platform_admin:post_list')
    extra_context = {'active': 'posts', 'title': 'Delete Blog Post', 'cancel_url': reverse_lazy('platform_admin:post_list')}


# ---------- Subjects (metadata only — full curriculum tree stays in /sd/) ----------

class SubjectListView(AdminListView):
    model = Subject
    ordering = ['order', 'name']
    extra_context = {
        'active': 'subjects',
        'title': 'Subjects',
        'columns': [('Name', 'name'), ('Theme', 'get_theme_display'), ('Order', 'order')],
        'create_url': None,
        'edit_url_name': 'platform_admin:subject_update',
        'delete_url_name': None,
        'note': 'Metadata only — units/lessons are edited in the real Django admin at /sd/.',
    }


class SubjectUpdateView(AdminUpdateView):
    model = Subject
    form_class = SubjectForm
    success_url = reverse_lazy('platform_admin:subject_list')
    extra_context = {'active': 'subjects', 'title': 'Edit Subject', 'cancel_url': reverse_lazy('platform_admin:subject_list')}


# ---------- Prelims Questions (with Choices inline formset) ----------

class QuestionListView(AdminListView):
    model = Question
    ordering = ['-created_at']
    extra_context = {
        'active': 'questions',
        'title': 'Prelims Questions',
        'columns': [('External ID', 'external_id'), ('Type', 'get_type_display'), ('Subject', 'subject'), ('Difficulty', 'difficulty')],
        'create_url': reverse_lazy('platform_admin:question_create'),
        'edit_url_name': 'platform_admin:question_update',
        'delete_url_name': 'platform_admin:question_delete',
    }


def _question_form_view(request, pk=None):
    instance = get_object_or_404(Question, pk=pk) if pk else None
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=instance)
        formset = ChoiceFormSet(request.POST, instance=instance or Question())
        if form.is_valid():
            question = form.save()
            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Question saved.')
                return redirect('platform_admin:question_list')
    else:
        form = QuestionForm(instance=instance)
        formset = ChoiceFormSet(instance=instance)

    return render(request, 'pages/platform_admin/question_form.html', {
        'active': 'questions',
        'title': 'Edit Question' if instance else 'New Question',
        'form': form,
        'formset': formset,
        'cancel_url': reverse_lazy('platform_admin:question_list'),
    })


class QuestionCreateView(StaffRequiredMixin, TemplateView):
    def get(self, request):
        return _question_form_view(request)

    def post(self, request):
        return _question_form_view(request)


class QuestionUpdateView(StaffRequiredMixin, TemplateView):
    def get(self, request, pk):
        return _question_form_view(request, pk)

    def post(self, request, pk):
        return _question_form_view(request, pk)


class QuestionDeleteView(AdminDeleteView):
    model = Question
    success_url = reverse_lazy('platform_admin:question_list')
    extra_context = {'active': 'questions', 'title': 'Delete Question', 'cancel_url': reverse_lazy('platform_admin:question_list')}


# ---------- Mains Questions ----------

class MainsQuestionListView(AdminListView):
    model = MainsQuestion
    ordering = ['-year', 'paper']
    extra_context = {
        'active': 'mains_questions',
        'title': 'Mains Questions',
        'columns': [('External ID', 'external_id'), ('Paper', 'paper'), ('Year', 'year'), ('Marks', 'marks')],
        'create_url': reverse_lazy('platform_admin:mains_question_create'),
        'edit_url_name': 'platform_admin:mains_question_update',
        'delete_url_name': 'platform_admin:mains_question_delete',
    }


class MainsQuestionCreateView(AdminCreateView):
    model = MainsQuestion
    form_class = MainsQuestionForm
    success_url = reverse_lazy('platform_admin:mains_question_list')
    extra_context = {'active': 'mains_questions', 'title': 'New Mains Question', 'cancel_url': reverse_lazy('platform_admin:mains_question_list')}


class MainsQuestionUpdateView(AdminUpdateView):
    model = MainsQuestion
    form_class = MainsQuestionForm
    success_url = reverse_lazy('platform_admin:mains_question_list')
    extra_context = {'active': 'mains_questions', 'title': 'Edit Mains Question', 'cancel_url': reverse_lazy('platform_admin:mains_question_list')}


class MainsQuestionDeleteView(AdminDeleteView):
    model = MainsQuestion
    success_url = reverse_lazy('platform_admin:mains_question_list')
    extra_context = {'active': 'mains_questions', 'title': 'Delete Mains Question', 'cancel_url': reverse_lazy('platform_admin:mains_question_list')}


# ---------- Users (read-only — account changes stay in /sd/) ----------

class UserListView(StaffRequiredMixin, ListView):
    model = User
    paginate_by = 25
    template_name = 'pages/platform_admin/user_list.html'
    ordering = ['-date_joined']
    extra_context = {'active': 'users', 'title': 'Users'}

    def get_queryset(self):
        return User.objects.filter(is_staff=False).select_related('profile').annotate(
            attempt_count=Count('attempts', distinct=True),
            bookmark_count=Count('bookmarks', distinct=True),
        )
