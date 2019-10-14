from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, CreateView
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
    if request.method == "POST":
        form = AddItemCategoryForm(request.POST)
        print(0)        
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = get_object_or_404(Seller, user__user=request.user)
            item.save()
            print(1)
            return redirect('add-product-step2', slug=item.slug)
    else:
        form = AddItemCategoryForm()

    return render(request, "products/add-category.html", {
        'form': form
    })

@login_required
@seller_required
def addProductStep2(request, slug):
    item = Item.objects.get(Q(slug=slug) & Q(seller__user__user=request.user))
    ImageFormSet = modelformset_factory(ItemImages, form=AddItemImagesForm, extra=3)
    if request.method == 'POST':
        # Seller Information form
        if 'seller_information' in request.POST:
            form = SellingInformation(request.POST)
            if form.is_valid():
                item.sku = form.cleaned_data['sku']
                item.stock = form.cleaned_data['stock']
                item.originalPrice = form.cleaned_data['originalPrice']
                item.gst = form.cleaned_data['gst']
                item.dispatch_time = form.cleaned_data['dispatch_time']
                item.listing_status = form.cleaned_data['listing_status']
                item.save()
                messages.success(request, f"Seller information updated")
                return redirect('add-product-step2', Item.objects.get(pk=item.id).slug)
            messages.warning(request, f"Seller information is not valid")
            return redirect('add-product-step2', Item.objects.get(pk=item.id).slug)
        # Product Description form
        if 'product_description' in request.POST:
            form = productDescription(request.POST)
            if form.is_valid():
                item.title = form.cleaned_data['title']
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
                messages.success(request, "Product Description added!")
                return redirect('add-product-step2', Item.objects.get(pk=item.id).slug)
            messages.warning(request, "Invalid information!")
            return redirect(request.path_info, Item.objects.get(pk=item.id).slug)
        # Package form
        if 'package_information' in request.POST:
            form = PackageDetailsForm(request.POST)
            if form.is_valid():
                thisPackage = PackageInformation.objects.filter(item=item)
                if len(thisPackage) == 0:
                    package = form.save(commit=False)
                    package.item = item
                    package.save()
                    messages.success(request, f"Package Information updated")
                    return redirect(request.path_info)
                thisPackage[0].packageLength = form.cleaned_data['packageLength']
                thisPackage[0].packageWidth = form.cleaned_data['packageWidth']
                thisPackage[0].packageHeight = form.cleaned_data['packageHeight']
                thisPackage[0].packageWeight = form.cleaned_data['packageWeight']
                thisPackage[0].save()
                messages.success(request, f"Package Information updated")
                return redirect('add-product-step2', Item.objects.get(pk=item.id).slug)
            messages.warning(request, f"Package information is not valid")
            return redirect('add-product-step2', Item.objects.get(pk=item.id).slug)

        if 'final_submit' in request.POST:
            item.finallySubmitted = True
            return redirect('view-all-product')
    else:
        seller_information = SellingInformation(instance=item)
        product_description = productDescription(instance=item)
        packageForm = PackageDetailsForm(instance=item)
        formset = ImageFormSet(queryset=ItemImages.objects.none())
    return render(request, "products/add-item.html", {
        'seller_information': seller_information,
        'product_description': product_description,
        'packageForm': packageForm,
        'formset': formset,
        'item': item
    })

@login_required
@seller_required
def uploadImages(request, slug):
    image = request.POST.get('image')
    formset = AddItemImagesForm(request.FILES or None)
    print(request.FILES)
    # if formset.is_valid():
    #     for f in formset:
    #         data = f.cleaned_data
    #         image = data.get('image')
    #         photo = ItemImages(image=image)
    #         photo.item = item
    #         photo.save()
    #         print("success")
    # item = Item.objects.get(slug=slug)
    # ItemImages.objects.create(item=item, image=image)
    content = {
        'success': "Image Uploaded"
    }
    return JsonResponse(content)

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
            images = ItemImages.objects.filter(
                Q(item__seller__user__user=request.user) & Q(item__slug=slug))
            for (f, i) in zip(formset, images):
                data = f.cleaned_data
                image = data.get('image')
                i.delete()
                ItemImages.objects.create(
                    item=Item.objects.get(slug=slug),
                    image=image
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
    tax = Charges.objects.get(category=category).gst
    charge = Charges.objects.get(category=category).serviceCharge
    data = {
        'tax': tax,
        'charge': charge
    }
    return JsonResponse(data)
