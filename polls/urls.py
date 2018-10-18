from django.urls import path
from . import views


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/electric/
    path('electric/', views.electric, name='electric'),
    # ex: /polls/electric/B1
    path('electric/<str:dashboard_id>', views.electricList,name='electricList'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
        # ex: /polls/api/1
    path('api/<int:cust_id>', views.api),


]
