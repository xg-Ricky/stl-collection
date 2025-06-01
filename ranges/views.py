from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def range_list(request):
    """List all ranges - staff only"""
    return render(request, 'ranges/list.html', {
        'message': 'Range management coming soon!'
    })
