from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from image_upload.models import Image
from image_upload.forms import ImageEditForm
from tags.models import Tag
import os

def gallery(request):
    """Gallery view with search and filtering"""
    images = Image.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        images = images.filter(
            Q(name__icontains=search_query) |
            Q(publisher__icontains=search_query) |
            Q(range__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
      # Filter by publisher
    publisher_filter = request.GET.get('publisher', '')
    if publisher_filter:
        images = images.filter(publisher__icontains=publisher_filter)
    
    # Filter by range
    range_filter = request.GET.get('range', '')
    if range_filter:
        images = images.filter(range__icontains=range_filter)
    
    # Filter by tags (AND logic - image must have ALL selected tags)
    tag_filter = request.GET.getlist('tags')
    if tag_filter:
        for tag in tag_filter:
            images = images.filter(tags=tag)
        images = images.distinct()
      # Get filter options for dropdowns
    publishers = Image.objects.exclude(
        Q(publisher__isnull=True) | Q(publisher__exact='')
    ).values_list('publisher', flat=True).distinct().order_by('publisher')
    
    ranges = Image.objects.exclude(
        Q(range__isnull=True) | Q(range__exact='')
    ).values_list('range', flat=True).distinct().order_by('range')
    all_tags = Tag.objects.all()
    
    # Pagination
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'collection/gallery.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'publisher_filter': publisher_filter,
        'range_filter': range_filter,
        'tag_filter': tag_filter,
        'publishers': publishers,
        'ranges': ranges,
        'all_tags': all_tags,
    })

@staff_member_required
def edit_image(request, image_id):
    """Edit an existing image - staff only"""
    image = get_object_or_404(Image, id=image_id)
    
    if request.method == 'POST':
        form = ImageEditForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated "{image.name}"!')
            return redirect('collection:gallery')
    else:
        form = ImageEditForm(instance=image)
    
    return render(request, 'collection/edit.html', {
        'form': form,
        'image': image
    })

@staff_member_required
def delete_image(request, image_id):
    """Delete an existing image - staff only"""
    image = get_object_or_404(Image, id=image_id)
    
    if request.method == 'POST':
        image_name = image.name
        
        # Delete the physical file if it exists
        if image.image:
            try:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path)
            except (ValueError, OSError) as e:
                # File doesn't exist or can't be deleted - log but continue
                messages.warning(request, f'Image file could not be deleted from disk, but database record was removed.')
        
        # Delete the database record
        image.delete()
        
        messages.success(request, f'Successfully deleted "{image_name}"!')
        return redirect('collection:gallery')
    
    # For GET requests, show confirmation page
    return render(request, 'collection/delete_confirm.html', {
        'image': image
    })
