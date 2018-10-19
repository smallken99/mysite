from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import DTSF01,DTSF02,DTSF03,DTSF04
from polls import  forms  

# Create your views here.

# ex: /polls/ 主頁
def index(request):
    DTSF01_list = DTSF01.objects.order_by("ROOM")
    return render(request, 'polls/index.html', locals())
# ex: /polls/api/1 房客基本資料
def api(request,cust_id):
	DTSF01_object = DTSF01.objects.get(pk=cust_id)
	data = serializers.serialize('json', [DTSF01_object,])
	return JsonResponse(data, safe=False)	
# ex: /polls/list/5 繳費清單
def list(request, dashboard_id):
    DTSF01vo = get_object_or_404(DTSF01, pk=dashboard_id)
    DTSF02_list = DTSF01vo.dtsf02_set.order_by("-INPUT_DATE")
    print(DTSF02_list)
    return render(request, 'polls/detail.html', locals())
# ex: /polls/api/bill/5 待繳費→已繳費
def bill(request,bill_id):
	downtown_store  = DTSF02.objects.get(pk=bill_id)
	downtown_store.IS_CONF = True
	status = downtown_store.save()
	data = {'STATUS': "OK" }
	return JsonResponse(data)

# ex: /polls/electric/ 公共電費
def electric(request):
    DTSF03_list = DTSF03.objects.order_by("DASHBOARD")
    return render(request, 'polls/index2.html', locals())    
# ex: /polls/electric/B1 公共電費清單
def electricList(request,dashboard_id):
	print("dashboard_id",dashboard_id)
	DTSF04_object = DTSF04.objects.filter(DASHBOARD=dashboard_id).order_by("-INPUT_DATE")[:10]
	return JsonResponse(serializers.serialize('json', DTSF04_object), safe=False)

def elec2db(request,dashboard_id):
	dtsf03 = DTSF03.objects.get(pk=dashboard_id)
	elec_form = forms.ElecForm()
	elec_form.fields['DASHBOARD'].initial = dtsf03.DASHBOARD
	elec_form.fields['INPUT_DATE'].initial = "2018-10-20"
	elec_form.fields['LAST_DEGREES'].initial = dtsf03.THIS_DEGREES
	elec_form.fields['THIS_DEGREES'].initial = dtsf03.THIS_DEGREES
	times = dtsf03.TIMES # 元/每度
	avg_num = dtsf03.AVG_NUM # 分攤人數
	message = "目前每度電費{}元，由{}人分攤" 
	message = message.format(times,avg_num)        
	return render(request, 'polls/elec2db.html', locals())