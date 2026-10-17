from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.prelims.models import Question

from .models import Bookmark


@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('question')
    return render(request, 'pages/engagement/bookmarks.html', {'bookmarks': bookmarks})


@login_required
@require_POST
def toggle_bookmark(request, pk):
    question = get_object_or_404(Question, pk=pk)
    bookmark = Bookmark.objects.filter(user=request.user, question=question).first()

    if bookmark:
        bookmark.delete()
        is_bookmarked = False
    else:
        Bookmark.objects.create(user=request.user, question=question)
        is_bookmarked = True

    return render(request, 'partials/engagement/bookmark_button.html', {
        'question': question,
        'is_bookmarked': is_bookmarked,
    })
