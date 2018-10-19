from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import DTSF01,DTSF02,DTSF03,DTSF04

# Create your views here.

# ex: /polls/ 主頁
def index(request):
    DTSF01_list = DTSF01.objects.order_by("ROOM")
    return render(request, 'polls/index.html', locals())
# ex: /polls/list/5 繳費清單
def list(request, dashboard_id):
    DTSF01vo = get_object_or_404(DTSF01, pk=dashboard_id)
    DTSF02_list = DTSF01vo.dtsf02_set.order_by("-INPUT_DATE")
    print(DTSF02_list)
    return render(request, 'polls/detail.html', locals())
# ex: /polls/api/bill/5 待繳費
def bill(request,bill_id):
	downtown_store  = DTSF02.objects.get(pk=bill_id)
	downtown_store.IS_CONF = True
	status = downtown_store.save()
	data = {'STATUS': "OK" }
	return JsonResponse(data)


def electric(request):
    DTSF03_list = DTSF03.objects.order_by("DASHBOARD")
    return render(request, 'polls/index2.html', locals())    

def electricList(request,dashboard_id):
	print("dashboard_id",dashboard_id)
	DTSF04_object = DTSF04.objects.filter(DASHBOARD=dashboard_id).order_by("-INPUT_DATE")[:10]
	return JsonResponse(serializers.serialize('json', DTSF04_object), safe=False)



 

def api(request,cust_id):
	DTSF01_object = DTSF01.objects.get(pk=cust_id)
	data = serializers.serialize('json', [DTSF01_object,])
	return JsonResponse(data, safe=False)		