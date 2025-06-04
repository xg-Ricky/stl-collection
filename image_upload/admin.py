from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Image

@admin.register(Image)
class ImageAdmin(ModelAdmin):
    list_display = ['name', 'publisher', 'range', 'upload_date']
    list_filter = ['publisher', 'range', 'upload_date', 'tags']
    search_fields = ['name', 'publisher', 'range', 'notes']
    filter_horizontal = ['tags']
    ordering = ['-upload_date']
    
    fieldsets = (
        ('File Information', {
            'fields': ('image', 'name')
        }),
        ('Metadata', {
            'fields': ('publisher', 'range', 'folder_location')
        }),
        ('Additional Information', {
            'fields': ('notes', 'tags')
        }),
    )
