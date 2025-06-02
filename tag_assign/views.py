from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
import json

from image_upload.models import Image
from tags.models import Tag, TagType

@staff_member_required
def assign_tags(request):
    """Bulk tag assignment interface - staff only"""
      # Get filter parameters
    search_query = request.GET.get('search', '')
    publisher_filter = request.GET.get('publisher', '')
    range_filter = request.GET.get('range', '')
    tag_filter = request.GET.get('tag_filter', '')
    tag_type_filter = request.GET.get('tag_type', '')
    missing_tag_type_filter = request.GET.get('missing_tag_type', '')
    untagged_only = request.GET.get('untagged_only') == 'on'
    
    # Start with all images
    images = Image.objects.all().prefetch_related('tags')
      # Apply filters
    if search_query:
        images = images.filter(
            Q(name__icontains=search_query) |
            Q(publisher__icontains=search_query) |
            Q(range__icontains=search_query)
        )
    
    if publisher_filter:
        images = images.filter(publisher=publisher_filter)
    
    if range_filter:
        images = images.filter(range=range_filter)
    
    if tag_filter:
        images = images.filter(tags__name=tag_filter)
    
    if untagged_only:
        images = images.filter(tags__isnull=True)
    
    # Filter for images missing any tags of a specific tag type
    if missing_tag_type_filter:
        try:
            tag_type_id = int(missing_tag_type_filter)
            # Get all images that have at least one tag of this type
            images_with_tag_type = Image.objects.filter(
                tags__tag_type_id=tag_type_id
            ).values_list('id', flat=True)
            # Exclude those images to get images without any tags of this type
            images = images.exclude(id__in=images_with_tag_type)
        except (ValueError, TypeError):
            # If conversion fails, ignore the filter
            pass
    
    # Order by upload date (newest first)
    images = images.order_by('-upload_date')
      # Pagination
    paginator = Paginator(images, 24)  # Show 24 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all available options for filters
    all_publishers = Image.objects.exclude(
        Q(publisher__isnull=True) | Q(publisher='')
    ).values_list('publisher', flat=True).distinct().order_by('publisher')
    
    all_ranges = Image.objects.exclude(
        Q(range__isnull=True) | Q(range='')
    ).values_list('range', flat=True).distinct().order_by('range')
    
    all_tags = Tag.objects.all().order_by('tag_type__sort_order', 'tag_type__name', 'name')
    
    # Filter quick tags by type if specified
    quick_tags = all_tags
    if tag_type_filter:
        try:
            tag_type_id = int(tag_type_filter)
            quick_tags = quick_tags.filter(tag_type_id=tag_type_id)
        except (ValueError, TypeError):
            # If conversion fails, show all tags
            pass
    
    # Get all tag types for the filter dropdown
    tag_types = TagType.objects.filter(is_active=True).order_by('sort_order', 'name')
      # Statistics
    total_images = Image.objects.count()
    untagged_count = Image.objects.filter(tags__isnull=True).count()
    tagged_count = total_images - untagged_count
    
    context = {
        'page_obj': page_obj,
        'all_publishers': all_publishers,
        'all_ranges': all_ranges,
        'all_tags': all_tags,
        'quick_tags': quick_tags,
        'tag_types': tag_types,
        'search_query': search_query,
        'publisher_filter': publisher_filter,
        'range_filter': range_filter,
        'tag_filter': tag_filter,
        'tag_type_filter': tag_type_filter,
        'missing_tag_type_filter': missing_tag_type_filter,
        'untagged_only': untagged_only,
        'total_images': total_images,
        'untagged_count': untagged_count,
        'tagged_count': tagged_count,
        'filtered_count': page_obj.paginator.count,
    }
    
    return render(request, 'tag_assign/assign.html', context)

@staff_member_required
@require_POST
def bulk_assign_tags(request):
    """Handle bulk tag assignment via AJAX"""
    try:
        data = json.loads(request.body)
        image_ids = data.get('image_ids', [])
        tag_ids = data.get('tag_ids', [])
        action = data.get('action', 'add')  # 'add' or 'remove'
        
        if not image_ids or not tag_ids:
            return JsonResponse({'success': False, 'error': 'Missing image IDs or tag IDs'})
        
        images = Image.objects.filter(id__in=image_ids)
        tags = Tag.objects.filter(id__in=tag_ids)
        
        affected_count = 0
        
        for image in images:
            if action == 'add':
                for tag in tags:
                    image.tags.add(tag)
                    affected_count += 1
            elif action == 'remove':
                for tag in tags:
                    image.tags.remove(tag)
                    affected_count += 1
        
        return JsonResponse({
            'success': True,
            'affected_count': affected_count,
            'message': f'Successfully {"added" if action == "add" else "removed"} tags for {len(images)} image(s)'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@staff_member_required
@require_POST  
def quick_tag_assign(request):
    """Quick single tag assignment via AJAX"""
    try:
        data = json.loads(request.body)
        image_id = data.get('image_id')
        tag_id = data.get('tag_id')
        action = data.get('action', 'toggle')  # 'toggle', 'add', or 'remove'
        
        if not image_id or not tag_id:
            return JsonResponse({'success': False, 'error': 'Missing image ID or tag ID'})
        
        image = get_object_or_404(Image, id=image_id)
        tag = get_object_or_404(Tag, id=tag_id)
        
        if action == 'toggle':
            if tag in image.tags.all():
                image.tags.remove(tag)
                assigned = False
            else:
                image.tags.add(tag)
                assigned = True
        elif action == 'add':
            image.tags.add(tag)
            assigned = True
        elif action == 'remove':
            image.tags.remove(tag)
            assigned = False
        
        return JsonResponse({
            'success': True,
            'assigned': assigned,
            'tag_count': image.tags.count()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
