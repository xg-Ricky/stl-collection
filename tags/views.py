from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Tag, TagType
from .forms import TagForm, TagTypeForm

@staff_member_required
def tag_list(request):
    """List all tags - staff only"""
    tags = Tag.objects.all()
    return render(request, 'tags/list.html', {
        'tags': tags,
        'active_tab': 'tags'
    })

@staff_member_required
def tagtype_list(request):
    """List all tag types - staff only"""
    tagtypes = TagType.objects.all()
    return render(request, 'tags/list.html', {
        'tagtypes': tagtypes,
        'active_tab': 'tagtypes'
    })

@staff_member_required
def create_tag(request):
    """Create a new tag - staff only"""
    # Get the tag type from URL parameter if creating another with same type
    tag_type_id = request.GET.get('tag_type_id')
    
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f'Successfully created tag "{tag.name}"!')
            
            # Check which button was clicked
            if 'create_another' in request.POST:
                # Redirect back to create page with the same tag type
                return redirect(f'{request.path}?tag_type_id={tag.tag_type.id}')
            else:
                return redirect('tags:list')
    else:
        # Initialize form with tag type if provided
        initial_data = {}
        if tag_type_id:
            try:
                tag_type = TagType.objects.get(id=tag_type_id)
                initial_data['tag_type'] = tag_type
            except TagType.DoesNotExist:
                pass
        
        form = TagForm(initial=initial_data)
    
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

@staff_member_required
def create_tagtype(request):
    """Create a new tag type - staff only"""
    if request.method == 'POST':
        form = TagTypeForm(request.POST)
        if form.is_valid():
            tagtype = form.save()
            messages.success(request, f'Successfully created tag type "{tagtype.name}"!')
            return redirect('tags:tagtype_list')
    else:
        form = TagTypeForm()
    
    return render(request, 'tags/create_tagtype.html', {
        'form': form
    })

@staff_member_required
def edit_tagtype(request, tagtype_id):
    """Edit an existing tag type - staff only"""
    tagtype = get_object_or_404(TagType, id=tagtype_id)
    
    if request.method == 'POST':
        form = TagTypeForm(request.POST, instance=tagtype)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated tag type "{tagtype.name}"!')
            return redirect('tags:tagtype_list')
    else:
        form = TagTypeForm(instance=tagtype)
    
    return render(request, 'tags/edit_tagtype.html', {
        'form': form,
        'tagtype': tagtype
    })

@staff_member_required
def delete_tagtype(request, tagtype_id):
    """Delete a tag type - staff only"""
    tagtype = get_object_or_404(TagType, id=tagtype_id)
    
    if request.method == 'POST':
        tagtype_name = tagtype.name
        # Check if there are tags using this type
        if tagtype.tags.exists():
            messages.error(request, f'Cannot delete tag type "{tagtype_name}" because it is being used by {tagtype.tags.count()} tag(s).')
            return redirect('tags:tagtype_list')
        
        tagtype.delete()
        messages.success(request, f'Successfully deleted tag type "{tagtype_name}"!')
        return redirect('tags:tagtype_list')
    
    return render(request, 'tags/delete_tagtype.html', {
        'tagtype': tagtype
    })
