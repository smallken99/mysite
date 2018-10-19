from django.urls import path
from . import views


urlpatterns = [
    # ex: /polls/ 主頁
    path('', views.index, name='index'),
    # ex: /polls/list/5 繳費清單
    path('list/<int:dashboard_id>', views.list, name='list'),
    # ex: /polls/api/bill/5 待繳費
    path('api/bill/<int:bill_id>', views.bill, name='bill'),

    # ex: /polls/electric/
    path('electric/', views.electric, name='electric'),
    # ex: /polls/electric/B1
    path('api/electric/<str:dashboard_id>', views.electricList,name='electricList'),

    # ex: /polls/api/1
    path('api/<int:cust_id>', views.api),


]
