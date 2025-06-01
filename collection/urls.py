from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('edit/<int:image_id>/', views.edit_image, name='edit'),
]
