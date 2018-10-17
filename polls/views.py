from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Question

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-room')[:5]
    return render(request, 'polls/index.html', locals())

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', locals())

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)	