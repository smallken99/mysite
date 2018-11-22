from django.shortcuts import get_object_or_404, render
import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import DTSF01,DTSF02,DTSF03,DTSF04
from polls import  forms  
import io
import xlsxwriter

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
	room = dtsf01.ROOM
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
	return HttpResponseRedirect('/polls/list/' + str(dtsf01_id))
	# message = "資料已新增!"
	# return render(request, 'ins2db.html', locals())

def excel(request,dashboard_id,input_date,cust_id):
	excel_name = dashboard_id + "_" + input_date + ".xlsx"
	output = io.BytesIO()  #用BytesIO 來存我們的資料
	workbook = xlsxwriter.Workbook(output)  #用xlsxwriter.Workbook來開啟我們剛剛建立的BytesIO
	worksheet = workbook.add_worksheet()  #新增一個sheet
	merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_name':'Arial'})
    # 'fg_color': 'yellow'})
	_format = workbook.add_format({
    'bold': 0,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_name':'Arial'})
	merge_format2 = workbook.add_format({
    'bold': 0,
    'border': 1,
    'align': 'left',
    'valign': 'vcenter'})
	worksheet.set_column('B:D', 12) #設定寬度
	worksheet.set_column('E:E', 35) #設定寬度
	# worksheet.set_row(3, 30) #設定高度
	worksheet.merge_range('B2:D2', dashboard_id + ' 房號   10-11 月份', merge_format) #合併 B2-D2 儲存格 
	worksheet.merge_range('B3:B7', '公共電費', merge_format)
	worksheet.merge_range('B8:B10', '個人電費', merge_format)
	worksheet.merge_range('B11:C11', '租金', merge_format)
	worksheet.merge_range('B12:C12', '合計', merge_format)

	worksheet.write(2,2,'上次電表',_format)
	worksheet.write(3,2,'本次電表',_format)
	worksheet.write(4,2,'用電數',_format)
	worksheet.write(5,2,'電費@3.5元',_format)
	worksheet.write(6,2,'平均每人',merge_format)
	worksheet.write(7,2,'上次電表',_format)
	worksheet.write(8,2,'本次電表',_format)
	worksheet.write(9,2,'個人電費',merge_format)

	DTSF04vo = DTSF04.objects.get(DASHBOARD=dashboard_id,INPUT_DATE=input_date)
	diff = DTSF04vo.THIS_DEGREES-DTSF04vo.LAST_DEGREES
	worksheet.write(2,3,DTSF04vo.LAST_DEGREES,_format)
	worksheet.write(3,3,DTSF04vo.THIS_DEGREES,_format)
	worksheet.write(4,3,str(diff),_format)
	worksheet.write(5,3,DTSF04vo.ELECTRIC_AMT,_format)
	worksheet.write(6,3,DTSF04vo.AVG_AMT,merge_format)

	DTSF01vo = DTSF01.objects.get(pk=cust_id)
	DTSF02vo = DTSF01vo.dtsf02_set.get(INPUT_DATE=input_date)
	worksheet.write(7,3,DTSF02vo.LAST_DEGREES,_format)
	worksheet.write(8,3,DTSF02vo.THIS_DEGREES,_format)
	worksheet.write(9,3,DTSF02vo.ELECTRIC_AMT,merge_format)
	worksheet.write(10,3,DTSF02vo.RENT_AMT,merge_format)
	worksheet.write(11,3,DTSF02vo.TOTAL_AMT,merge_format)

	worksheet.merge_range('E2:E12', "連絡人: 許小姐 \nEmail: oioi7211@gmail.com \n手機: 0921-584584 \n匯入帳號: 渣打銀行 南京分行 \
                      \n\t銀行代碼 : 052 \n\t帳號 : 1122 00000 33738 \n戶名:黃棋新 \n\n\n請於30號前匯入 , 若有其他問題\n請來電 , 謝謝!   ", merge_format2)
	workbook.close()  #把workbook關閉
	output.seek(0)
	response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=" + excel_name;
	return response

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