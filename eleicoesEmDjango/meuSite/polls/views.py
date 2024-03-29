from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question,Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selecte_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Selecione alguma opção"
            }
        )
    else:
        selecte_choice.votes = F("votes") + 1
        selecte_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))