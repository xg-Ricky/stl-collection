from django.urls import path
from . import views

app_name = 'ranges'

urlpatterns = [
    path('', views.range_list, name='list'),
    path('<str:range_name>/', views.range_detail, name='detail'),
]
