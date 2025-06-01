from django.urls import path
from . import views

app_name = 'tag_assign'

urlpatterns = [
    path('', views.assign_tags, name='assign'),
]
