from django.db.models import Count
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from .models import Board, Topic, Comment
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import NewTopicForm, CommentForm
from django.views.generic import UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


def about(request):
    return HttpResponse('about page')


def boards_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    queryset = board.topics.annotate(replies=Count('comments'))
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics/topics.html', {'board': board, 'topics': topics})


@login_required
def add_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    form = NewTopicForm()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()

            comment = Comment.objects.create(
                message=form.cleaned_data.get('message'),
                created_by=request.user,
                topic=topic
            )
            return redirect('board_topics', board_id=board.pk)

    return render(request, 'topics/add_topic.html', {'board': board, 'form': form})


def topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)

    session_key = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True

    return render(request, 'topics/topic.html', {'topic': topic})


@login_required()
def topic_reply(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.created_by = request.user
            comment.save()

            topic.updated_at = timezone.now()
            topic.save()

            return redirect('topic', board_id=board_id, topic_id=topic.pk)
    return render(request, 'topics/topic_reply.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Comment
    fields = ('message',)
    template_name = 'comments/edit_comment.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.updated_at = timezone.now()
        comment.updated_by = self.request.user
        comment.save()
        return redirect('topic', board_id=comment.topic.board.pk, topic_id=comment.topic.pk)



