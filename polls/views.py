"""View for web application."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    """ListView class for IndexView."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Get queryset questions for IndexView.

        Returns:
            published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    """DetailView class for DetailView."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet.

        Returns:
            questions that aren's published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """DetailView class for ResultsView."""

    model = Question
    template_name = 'polls/results.html'


def index(request):
    """Get a request for index.

    Args:
        request: is a request for the page.

    Returns:
        a page for index.
    """
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Get a detail for voting page.

    Args:
        request: is a request for the page
        question_id: is a question_id of the question object model.

    Returns:
        a page for detail.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """Get a results for results page.

    Args:
        request: is a request for the page
        question_id: is a question_id of the question object model.

    Returns:
        a page for results.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """Vote increment and get vote results page.

    Args:
        request: is a request for the page
        question_id: is a question_id of the question object model.

    Returns:
        a page for the status of the vote.

    Raises:
        KeyError if any choice was not chosen.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,)))


def vote_for_poll(request, question_id):
    """Vote results page for the poll.

    Args:
        request: is a request for the page
        question_id: is a question_id of the question object model.

    Returns:
        redirect page for someplace if the question_id does not exist.
        redirect page for that question if the question_if exist.
    """
    choice_id = request.POST['choice']
    if not choice_id:
        messages.error(request, "You didn't make a choice")
        return redirect('polls:someplace')

    messages.success(request, "Your choice successfully recorded. Thank you.")
    return redirect('polls:results')
