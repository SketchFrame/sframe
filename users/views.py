from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import UserExtended
from products.models import Order
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from affiliate.models import Affiliate
from .models import Address, UserExtended
from .forms import AddAddressForm, AddPaymentNumbersForm
from bids.models import project

@login_required
def addAddress(request):
    if request.method == "POST":
        form = AddAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = get_object_or_404(UserExtended, user=request.user)
            address.save()
            return redirect('account_profile')
        else:
            messages.warning(request, "Invalid Data Entered!")
            return redirect(request.path_info)
    else:
        form = AddAddressForm()
    return render(request, "users/add-edit-address.html", {
        'form': form,
        'text': "Add Address"
    })
    

@login_required
def delAddress(request, pk):
    Address.objects.get(Q(user__user=request.user) & Q(pk=pk)).delete()
    messages.success(request, 'Address deleted.')
    return redirect('account_profile')


@login_required
def editAddress(request, pk):
    address = Address.objects.get(Q(user__user=request.user) & Q(pk=pk))
    if request.method == "POST":
        form = AddAddressForm(request.POST)
        if form.is_valid():
            address.address1 = form.cleaned_data['address1']
            address.address2 = form.cleaned_data['address2']
            address.landmark = form.cleaned_data['landmark']
            address.phone1 = form.cleaned_data['phone1']
            address.phone2 = form.cleaned_data['phone2']
            address.state = form.cleaned_data['state']
            address.country = form.cleaned_data['country']
            address.city = form.cleaned_data['city']
            address.zipCode = form.cleaned_data['zipCode']
            address.save()
            messages.info(request, "Address Updated")
            return redirect("account_profile")
        else:
            messages.warning(request, "Invalid data")
            return redirect("account_profile")
    else:
        form = AddAddressForm(initial={
            'address1': address.address1,
            'address2': address.address2,
            'landmark': address.landmark,
            'phone1': address.phone1,
            'phone2': address.phone2,
            'state': address.state,
            'country': address.country,
            'city': address.city,
            'zipCode': address.zipCode
        })
    return render(request, "users/add-edit-address.html", {'form': form, 'text': 'Edit Address'})


@login_required
def profile(request):
    context = {}
    if request.method == "POST":
        if 'paytm' in request.POST:
            form = AddPaymentNumbersForm(request.POST)
            if form.is_valid():
                user = UserExtended.objects.get(user=request.user)
                user.paytm_number = form.cleaned_data['paytm_number']
                user.save()
                messages.success(request, "Paytm Number changes done")
                return redirect(request.path_info)
            else:
                messages.warning(request, "Data entered was not valid!")
                return redirect(request.path_info)
        elif 'google-pay' in request.POST:
            form = AddPaymentNumbersForm(request.POST)
            if form.is_valid():
                user = UserExtended.objects.get(user=request.user)
                user.googlePay_number = form.cleaned_data['googlePay_number']
                user.save()
                messages.success(request, "Google Pay UPI ID changes done")
                return redirect(request.path_info)
            else:
                messages.warning(request, "Data entered was not valid!")
                return redirect(request.path_info)
        
        elif 'remove-google-pay' in request.POST:
            user = UserExtended.objects.get(user=request.user)
            user.googlePay_number = None
            user.save()
            messages.success(request, "Google Pay UPI ID removed")
            return redirect(request.path_info)

        elif 'remove-paytm' in request.POST:
            user = UserExtended.objects.get(user=request.user)
            user.paytm_number = None
            user.save()
            messages.success(request, "Paytm number removed")
            return redirect(request.path_info)
    else:
        form = AddPaymentNumbersForm()
    user = request.user
    userExt = UserExtended.objects.filter(
        user__username=user.username).first()
    
    CompleteOrders = Order.objects.filter(
        Q(user__username=user.username) & Q(ordered=True))
    if len(CompleteOrders) > 0:
        context.update({
            'CompleteOrders': CompleteOrders,
        })
    
    IncompleteOrders = Order.objects.filter(
        Q(user__username=user.username) & Q(ordered=False))
    if len(IncompleteOrders) > 0:
        context.update({
            'IncompleteOrders': IncompleteOrders,
        })
    
    affiliates = Affiliate.objects.filter(user__user=request.user)
    if len(affiliates) > 0:
        context.update({
            'affiliates': affiliates
        })
    
    addresses = Address.objects.filter(user__user=request.user)
    posted_projects = project.objects.filter(user__user=request.user)
    context.update({
        'user': user,
        'userExt': userExt,
        'addresses': addresses,
        'projects': posted_projects,
        'form': form,
        'paytm': userExt.paytm_number,
        'google_pay':userExt.googlePay_number,
    })
    return render(request, 'account/profile.html', context)
