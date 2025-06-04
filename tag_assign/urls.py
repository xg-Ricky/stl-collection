from django.urls import path
from . import views

app_name = 'tag_assign'

urlpatterns = [
    path('', views.assign_tags, name='assign'),
    path('bulk-assign/', views.bulk_assign_tags, name='bulk_assign'),
    path('quick-assign/', views.quick_tag_assign, name='quick_assign'),
]
