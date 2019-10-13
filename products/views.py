from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q
from .models import Item, ItemImages, OrderItem
from .forms import *
from seller.models import Seller
from seller.decorators import seller_required
from core.models import Charges
from django.http import JsonResponse
import os


@login_required
@seller_required
def addProductStep1(request):
    incompleteItems = Item.objects.filter(
        Q(seller__user__user=request.user) & Q(finallySubmitted=False)).count()
    if incompleteItems > 0:
        messages.warning(
            request, f"You already have {incompleteItems} incomplete artworks.")
        return redirect('view-all-product')
    if request.method == "POST":
        form = AddItemCategoryForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = get_object_or_404(Seller, user__user=request.user)
            item.save()
            return redirect('add-product-step2', slug=item.slug)
    else:
        form = AddItemCategoryForm()

    return render(request, "products/add-category.html", {
        'form': form
    })


@login_required
@seller_required
def addProductStep2(request, slug):
    ImageFormSet = modelformset_factory(
        ItemImages, form=AddItemImagesForm, extra=3)
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        packageForm = PackageDetailsForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid() and packageForm.is_valid():

            item = get_object_or_404(Item, slug=slug)

            item.title = form.cleaned_data['title']
            item.sku = form.cleaned_data['sku']
            item.stock = form.cleaned_data['stock']

            item.originalPrice = form.cleaned_data['originalPrice']
            item.price = form.cleaned_data['price']
            item.discount = form.cleaned_data['discount']
            item.gst = form.cleaned_data['gst']

            item.dispatch_time = form.cleaned_data['dispatch_time']
            item.listing_status = form.cleaned_data['listing_status']
            item.color = form.cleaned_data['color']

            item.shortDescription = form.cleaned_data['shortDescription']
            item.fullDescription = form.cleaned_data['fullDescription']

            item.weight = form.cleaned_data['weight']
            item.length = form.cleaned_data['length']
            item.height = form.cleaned_data['height']

            item.hsnCode = form.cleaned_data['hsnCode']
            item.frameCost = form.cleaned_data['frameCost']
            item.addFrame = form.cleaned_data['addFrame']
            item.save()

            package = packageForm.save(commit=False)
            package.item = item
            package.save()

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
        packageForm = PackageDetailsForm()
        formset = ImageFormSet(queryset=ItemImages.objects.none())
    return render(request, "products/add-item.html", {
        'form': form,
        'packageForm': packageForm,
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
    withImages = []
    items = Item.objects.filter(
        seller__user__user__username=request.user.username)
    images = ItemImages.objects.filter(
        item__seller__user__user__username=request.user.username)
    for item in items:
        for image in images:
            if item.slug == image.item.slug:
                withImages.append(item)
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break

    for item in items:
        if item not in withImages:
            d.update({'item': item, 'image': 'No Image'})
            l.append(d.copy())

    return render(request, 'products/view-all-products.html', {
        'products': l
    })

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
