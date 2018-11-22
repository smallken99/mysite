from django.urls import path
from . import views


urlpatterns = [
    # ex: /polls/ 主頁 tab1
    path('', views.index, name='index'),
    # ex: /polls/api/1 房客基本資料
    path('api/<int:cust_id>', views.api),    
    # ex: /polls/list/5 繳費清單
    path('list/<int:dashboard_id>', views.list, name='list'),
    # ex: /polls/api/bill/5 待繳費
    path('api/bill/<int:bill_id>', views.bill, name='bill'),
    # ex: /polls/ins/5 個人電費 新增繳費 預備新增
    path('ins/<int:pk_id>', views.ins, name='ins'),
    # ex: /polls/insto 個人電費 新增繳費 實際新增
    path('insto', views.insto, name='insto'),
    # ex: /polls/excel/B1/2018-08-03/2 產生電費小紙條
    path('excel/<str:dashboard_id>/<str:input_date>/<int:cust_id>', views.excel, name='excel'), 

    # ex: /polls/electric/ 公共電費 tab2
    path('electric/', views.electric, name='electric'),
    # ex: /polls/electric/B1 公共電費清單
    path('api/electric/<str:dashboard_id>', views.electricList,name='electricList'),
    # ex: /polls/electric/ins/B1 公共電費 新增繳費 預備新增
    path('electric/ins/<str:dashboard_id>', views.elec_ins, name='elec_ins'),
    # ex: /polls/electric/insto 公共電費 新增繳費 實際新增
    path('electric/insto', views.elec_insto, name='elec_insto'),


]
