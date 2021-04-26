from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View
from .models import Choice, Question, Comment, Tag
from .forms import CommentForm
from django.db.models import F, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import views as auth_views
from django.conf import settings


User = settings.AUTH_USER_MODEL


class IndexView(generic.ListView):
    """
        lists poll questions  :model:`polls.Question`.

        **Template:**

        :template:`polls/index.html`
        """
    template_name = 'polls/index.html'

    def get(self, request):
        latest_question_list = Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('priority')[:5]
        popular_polls = \
            Question.objects.annotate(num_votes=Sum('choice__votes')).filter(
                num_votes__isnull=False).order_by(
                '-num_votes')[0]
        return render(request, 'polls/index.html',
                      {'latest_question_list': latest_question_list,
                       'popular_polls': popular_polls, })


class DetailView(generic.DetailView):
    """
        Display Choices for a selected question and lists comments for that question :model:`polls.Question`
        model:`Choice' and model: 'Comment'.

        **Template:**

        :template:`polls/detail.html`
    """
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        if question.is_expired:
            return HttpResponseRedirect(
                reverse('polls:results', args=(question.id,)))
        else:
            self.update_view_count(request, question_id)
            comments = Comment.objects.filter(question=question_id)
            comment_form = CommentForm()
            return render(request, 'polls/detail.html', {'question': question,
                                                         'comments': comments,
                                                         'comment_form': comment_form,
                                                         })

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return self.save_comment(request, question_id)

    def update_view_count(self, request, question_id):
        Question.objects.filter(pk=question_id).update(
            view_count=F('view_count') + 1)

    def save_comment(self, request, question_id):
        template_name = 'polls/detail.html'
        question = get_object_or_404(Question, pk=question_id)
        comments = Comment.objects.filter(question=question_id)
        new_comment = None
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.question = question
                new_comment.save()
        else:
            comment_form = CommentForm()
        return render(request, template_name, {'question': question,
                                               'comments': comments,
                                               'new_comment': new_comment,
                                               'comment_form': comment_form,
                                               })


class ResultsView(generic.DetailView):
    """
        lists choices and total votes  :model:`polls.Question`.

         **Template:**

        :template:`polls/results.html`
    """
    model = Question
    template_name = 'polls/results.html'


class VoteView(generic.ListView):
    """
        increments vote value for selected choice
    """

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        try:
            selected_choice = question.choice.get(
                pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(
                reverse('polls:results', args=(question.id,)))

