from django.urls import path
from . import views


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/elec/
    path('electric/', views.electric, name='electric'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
        # ex: /polls/api/cusData/
    path('api/<int:cust_id>', views.api),
]
