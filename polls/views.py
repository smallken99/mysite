from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import DTSF01,DTSF03

# Create your views here.

def index(request):
    DTSF01_list = DTSF01.objects.order_by("ROOM")
    return render(request, 'polls/index.html', locals())

def electric(request):
    DTSF03_list = DTSF03.objects.order_by("DASHBOARD")
    return render(request, 'polls/index2.html', locals())    

def detail(request, room_id):
    DTSF01vo = get_object_or_404(DTSF01, pk=room_id)
    return render(request, 'polls/detail.html', locals())

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)	

def api(request,cust_id):
	DTSF01_object = DTSF01.objects.get(pk=cust_id)
	data = serializers.serialize('json', [DTSF01_object,])
	return JsonResponse(data, safe=False)		