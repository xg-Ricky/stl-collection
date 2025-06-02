from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Tag, TagType

@admin.register(TagType)
class TagTypeAdmin(ModelAdmin):
    list_display = ['name', 'color', 'sort_order', 'is_active', 'tag_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['sort_order', 'name']
    list_editable = ['sort_order', 'is_active']
    
    def tag_count(self, obj):
        return obj.tags.count()
    tag_count.short_description = 'Tags'

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'tag_type', 'usage_count', 'created_at']
    list_filter = ['tag_type', 'created_at']
    search_fields = ['name']
    ordering = ['tag_type__sort_order', 'tag_type__name', 'name']
    
    def usage_count(self, obj):
        return obj.image_set.count()
    usage_count.short_description = 'Usage Count'
