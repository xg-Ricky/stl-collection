from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def assign_tags(request):
    """Assign tags to images - staff only"""
    return render(request, 'tag_assign/assign.html', {
        'message': 'Bulk tag assignment coming soon!'
    })
