from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question

def index(request):
  latest_questions = Question.objects.order_by('-date')
  context = {'latest_questions': latest_questions}
  print(latest_questions[0].id)
  return render(request, 'polls/index.html', context)


def detail(request, question_id):
  question = Question.objects(id=question_id)
  return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
  question = Question.objects(id=question_id)
  return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
  question = Question.objects(id=question_id)
  try:
    choice_position = int(request.POST['choice']) - 1
    print("AQUI", choice_position)
    selected_choice = question.choices[choice_position]
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    question.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
