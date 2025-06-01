from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Tag
from .forms import TagForm

@staff_member_required
def tag_list(request):
    """List all tags - staff only"""
    tags = Tag.objects.all()
    return render(request, 'tags/list.html', {
        'tags': tags
    })

@staff_member_required
def create_tag(request):
    """Create a new tag - staff only"""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f'Successfully created tag "{tag.name}"!')
            return redirect('tags:list')
    else:
        form = TagForm()
    
    return render(request, 'tags/create.html', {
        'form': form
    })

@staff_member_required
def edit_tag(request, tag_id):
    """Edit an existing tag - staff only"""
    tag = get_object_or_404(Tag, id=tag_id)
    
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated tag "{tag.name}"!')
            return redirect('tags:list')
    else:
        form = TagForm(instance=tag)
    
    return render(request, 'tags/edit.html', {
        'form': form,
        'tag': tag
    })

@staff_member_required
def delete_tag(request, tag_id):
    """Delete a tag - staff only"""
    tag = get_object_or_404(Tag, id=tag_id)
    
    if request.method == 'POST':
        tag_name = tag.name
        tag.delete()
        messages.success(request, f'Successfully deleted tag "{tag_name}"!')
        return redirect('tags:list')
    
    return render(request, 'tags/delete.html', {
        'tag': tag
    })
