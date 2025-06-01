from django.urls import path
from . import views

app_name = 'ranges'

urlpatterns = [
    path('', views.range_list, name='list'),
]
