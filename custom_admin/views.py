from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from products.models import Item

@staff_member_required
def admin_dashboard(request):
    return render(request, 'custom_admin/admin-dashboard.html')

@staff_member_required
def refresh_charges(request):
    try:
        items = Item.objects.all()
        for item in items:
            item.save()
        messages.success(request, "All items refreshed Successfully.")
    except:
        messages.warning(request, "Something went wrong.")
    return redirect('admin-dashboard')

