from django.shortcuts import get_object_or_404, render
import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import DTSF01,DTSF02,DTSF03,DTSF04
from polls import  forms  

# Create your views here.

# ex: /polls/ 主頁
def index(request):
	DTSF01_list = DTSF01.objects.filter(STATUS='Y').order_by("ROOM")
	After45days =  datetime.datetime.now() + datetime.timedelta(days=45)
	# 找還有未繳費的紀錄,要標示
	for vo in DTSF01_list:
		endDate = datetime.datetime(int(vo.END_DATE[:4]),int(vo.END_DATE[5:7]),int(vo.END_DATE[-2:]))
		if After45days > endDate:
			vo.DAYLINE = True
		dtsf02_list = vo.dtsf02_set.all()
		for dtsf02 in dtsf02_list:
			if dtsf02.IS_CONF == False:
				vo.IS_CONF = False
	return render(request, 'index.html', locals())

# ex: /polls/api/1 房客基本資料
def api(request,cust_id):
	DTSF01_object = DTSF01.objects.get(pk=cust_id)
	data = serializers.serialize('json', [DTSF01_object,])
	return JsonResponse(data, safe=False)	
# ex: /polls/list/5 繳費清單
def list(request, dashboard_id):
    DTSF01vo = get_object_or_404(DTSF01, pk=dashboard_id)
    DTSF02_list = DTSF01vo.dtsf02_set.order_by("-INPUT_DATE","-pk")
    # print(DTSF02_list)
    return render(request, 'detail.html', locals())
# ex: /polls/api/bill/5 待繳費→已繳費
def bill(request,bill_id):
	downtown_store  = DTSF02.objects.get(pk=bill_id)
	downtown_store.IS_CONF = True
	downtown_store.save()
	data = {'STATUS': "OK" }
	return JsonResponse(data)
# ex: /polls/electric/ins/B1 公共電費 新增繳費 預備新增
def ins(request,pk_id):
	action = "init"
	dtsf01 = DTSF01.objects.get(pk=pk_id)
	dtsf02_form = forms.DTSF02Form()
	dtsf02_form.fields['DTSF01'].initial = pk_id
	dtsf02_form.fields['INPUT_DATE'].initial = datetime.datetime.now().strftime("%Y-%m-%d")
	dtsf02_form.fields['LAST_DEGREES'].initial = dtsf01.THIS_DEGREES
	dtsf02_form.fields['THIS_DEGREES'].initial = dtsf01.THIS_DEGREES
	dtsf02_form.fields['RENT_AMT'].initial = dtsf01.RENT_AMT
	pub_dashboard = dtsf01.PUB_DASHBOARD
	times = dtsf01.TIMES # 元/每度
	message = "計算公式,目前每度電費{}元" 
	message = message.format(times)        
	return render(request, 'ins2db.html', locals())

def insto(request):
	dtsf02_form = forms.DTSF02Form()
	dtsf01_id = ""
	if request.method == 'POST':
		form = forms.DTSF02Form(request.POST)
		if form.is_valid():
			form.save()
			print("save bill")
			#更新最近電表度數
			dtsf01_id = form['DTSF01'].value()
			this_degrees = form['THIS_DEGREES'].value()
			dtsf01vo = DTSF01.objects.get(pk=dtsf01_id)
			dtsf01vo.THIS_DEGREES = this_degrees
			dtsf01vo.save()
			print("save THIS_DEGREES",dtsf01vo.THIS_DEGREES)
			# return HttpResponseRedirect('/polls/list/' + str(dtsf02_form.cleaned_data['DTSF01'].pk))
	message = "資料已新增!"
	return render(request, 'ins2db.html', locals())



# ex: /polls/electric/ 公共電費
def electric(request):
    DTSF03_list = DTSF03.objects.order_by("DASHBOARD")
    return render(request, 'index2.html', locals())    
# ex: /polls/electric/B1 公共電費清單
def electricList(request,dashboard_id):
	print("dashboard_id",dashboard_id)
	DTSF04_object = DTSF04.objects.filter(DASHBOARD=dashboard_id).order_by("-INPUT_DATE")[:10]
	return JsonResponse(serializers.serialize('json', DTSF04_object), safe=False)
# ex: /polls/electric/ins/B1 公共電費 新增繳費 預備新增
def elec_ins(request,dashboard_id):
	dtsf03 = DTSF03.objects.get(pk=dashboard_id)
	elec_form = forms.DTSF04Form()
	elec_form.fields['DASHBOARD'].initial = dtsf03.DASHBOARD
	elec_form.fields['INPUT_DATE'].initial = datetime.datetime.now().strftime("%Y-%m-%d")
	elec_form.fields['LAST_DEGREES'].initial = dtsf03.THIS_DEGREES
	elec_form.fields['THIS_DEGREES'].initial = ""
	times = dtsf03.TIMES # 元/每度
	avg_num = dtsf03.AVG_NUM # 分攤人數
	message = "目前每度電費{}元，由{}人分攤" 
	message = message.format(times,avg_num)        
	return render(request, 'elec2db.html', locals())

def elec_insto(request):
	elec_form = forms.DTSF04Form()
	if request.method == 'POST':
		form = forms.DTSF04Form(request.POST)
		ROOM = form['DASHBOARD'].value()
		THIS_DEGREES = form['THIS_DEGREES'].value()
		print(THIS_DEGREES)
		if form.is_valid():
			form.save()
			print("save bill")
			#更新最近電表度數
			dtsf03vo = DTSF03.objects.get(DASHBOARD = ROOM)
			dtsf03vo.THIS_DEGREES = THIS_DEGREES
			dtsf03vo.save()
			print("save THIS_DEGREES",dtsf03vo.THIS_DEGREES)
			# return HttpResponseRedirect('/list/')
	message = "已成功新增!"
	return render(request, 'elec2db.html', locals())