from django.shortcuts import render
from image_upload.models import Image
from tags.models import Tag

def landing_page(request):
    """Landing page showing the latest 4 uploaded images"""
    latest_images = Image.objects.order_by('-upload_date')[:4]
    
    # Statistics
    total_images = Image.objects.count()
    total_tags = Tag.objects.count()
    total_publishers = Image.objects.exclude(publisher__isnull=True).exclude(publisher__exact='').values('publisher').distinct().count()
    total_ranges = Image.objects.exclude(range__isnull=True).exclude(range__exact='').values('range').distinct().count()
    
    return render(request, 'landing_page.html', {
        'latest_images': latest_images,
        'total_images': total_images,
        'total_tags': total_tags,
        'total_publishers': total_publishers,
        'total_ranges': total_ranges,
    })
