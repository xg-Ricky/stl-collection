from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Tag

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']
