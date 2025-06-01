from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ImageUploadForm
from .models import Image

@staff_member_required
def upload_image(request):
    """Upload a new image - staff only"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            messages.success(request, f'Successfully uploaded "{image.name}"!')
            return redirect('image_upload:upload')
    else:
        form = ImageUploadForm()
    
    return render(request, 'image_upload/upload.html', {
        'form': form
    })
