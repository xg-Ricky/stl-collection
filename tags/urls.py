from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [
    path('', views.tag_list, name='list'),
    path('create/', views.create_tag, name='create'),
    path('edit/<int:tag_id>/', views.edit_tag, name='edit'),
    path('delete/<int:tag_id>/', views.delete_tag, name='delete'),
]
