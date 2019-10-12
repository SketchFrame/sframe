from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q
from .models import Item, ItemImages, OrderItem
from .forms import AddItemForm, AddItemImagesForm, EditProductImagesForm, EditProduct
from seller.models import Seller
from seller.decorators import seller_required
from core.models import Charges
from django.http import JsonResponse
import os

@login_required
@seller_required
def addProduct(request):
    ImageFormSet = modelformset_factory(
        ItemImages, form=AddItemImagesForm, extra=3)
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.seller = get_object_or_404(
                Seller, user__user__username=request.user.username)
            item.save()
            for f in formset:
                data = f.cleaned_data
                image = data.get('image')
                photo = ItemImages(image=image)
                photo.item = item
                photo.save()
                print("success")
            return redirect("view-product", slug=item.slug)
    else:
        form = AddItemForm()
        formset = ImageFormSet(queryset=ItemImages.objects.none())
    return render(request, "products/add-item.html", {
        'form': form,
        'formset': formset
    })

@login_required
@seller_required
def viewProduct(request, slug):
    item = Item.objects.get(slug=slug)
    itemImages = ItemImages.objects.filter(item=item)
    return render(request, "products/view-item.html", {
        'item': item,
        'itemImages': itemImages
    })

@method_decorator([login_required, seller_required], name='dispatch')
class ProductUpdateView(UpdateView):
    model = Item
    template_name = "products/edit-item.html"
    form_class = EditProduct
    success_url = '/seller/view-product/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ItemImages.objects.filter(
            item__slug=self.kwargs['slug'])
        context['product_slug'] = self.kwargs['slug']
        return context

@login_required
@seller_required
def ProductImagesUpdate(request, slug):
    ImageFormSet = modelformset_factory(
        ItemImages, form=EditProductImagesForm, extra=3)

    if request.method == 'POST':
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if formset.is_valid():
            images = ItemImages.objects.filter(Q(item__seller__user__user=request.user) & Q(item__slug=slug))
            for (f, i) in zip(formset, images):
                data = f.cleaned_data
                image = data.get('image')
                i.delete()
                ItemImages.objects.create(
                    item = Item.objects.get(slug=slug),
                    image = image
                )
            return redirect("view-product", slug=slug)

    else:
        formset = ImageFormSet(queryset=ItemImages.objects.none())
    return render(request, "products/edit-images.html", {
        'form': formset
    })

@method_decorator([login_required, seller_required], name="dispatch")
class ProductDeleteView(DeleteView):
    model = Item
    template_name = "products/delete-item.html"
    success_url = '/product/add-product'

@login_required
@seller_required
def viewAllProduct(request):
    l = []
    d = {}
    items = Item.objects.filter(
        seller__user__user__username=request.user.username)
    images = ItemImages.objects.filter(
        item__seller__user__user__username=request.user.username)
    for item in items:
        sale = 0
        orderItems = OrderItem.objects.filter(
            Q(ordered=True) & Q(item=item))
        if len(orderItems) > 0:
            for orderItem in orderItems:
                qty = orderItem.quantity
                if item.discount_price:
                    sale += item.originalDiscount_price * qty
                else:
                    sale += item.originalPrice * qty
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image, 'sale': sale})
                l.append(d.copy())
                break
    context = {
        'products': l
    }
    return render(request, 'products/view-all-products.html', context)

@login_required
@seller_required
def get_charges(request):
    category = request.POST.get('category')
    if category == '':
        data = {
            'error': "Category was not given"
        }
        return JsonResponse(data)
    tax = Charges.objects.get(category = category).gst
    charge = Charges.objects.get(category = category).serviceCharge
    data = {
        'tax': tax,
        'charge': charge
    }
    return JsonResponse(data)
