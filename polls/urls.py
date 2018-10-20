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

    # ex: /polls/electric/ 公共電費 tab2
    path('electric/', views.electric, name='electric'),
    # ex: /polls/electric/B1 公共電費清單
    path('api/electric/<str:dashboard_id>', views.electricList,name='electricList'),
    # ex: /polls/electric/ins/B1 公共電費 新增繳費 預備新增
    path('electric/ins/<str:dashboard_id>', views.ins, name='ins'),
    # ex: /polls/electric/insto 公共電費 新增繳費 實際新增
    path('electric/insto', views.insto, name='insto'),


]
