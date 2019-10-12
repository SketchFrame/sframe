from django.shortcuts import render, get_object_or_404, redirect
from users.models import UserExtended
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ProductAffiliate, Affiliate
from django.contrib import messages
from shop.views import addToCart
from products.models import OrderItem, Item
from django.db.models import Q

@login_required
def register(request):
    user = get_object_or_404(UserExtended, user=request.user)
    if user.is_refering == False:
        if request.method == 'POST':
            user.is_refering = True
            user.save()
            return redirect("register-affiliate")
        return render(request, 'affiliate/register.html')
    else:
        return redirect('affiliate-options')

@login_required
def affiliate_options(request):
    sellerAffiliates = Affiliate.objects.filter(user__user=request.user)
    productAffiliates = ProductAffiliate.objects.filter(user__user=request.user)
    
    sellerAffiliatesAmount = 0
    for sellerAffiliate in sellerAffiliates:
        sellerAffiliatesAmount += sellerAffiliate.amount
    sellerAffiliatesAmount = round(sellerAffiliatesAmount, 2)

    productAffiliateAmount = 0
    for productAffiliate in productAffiliates:
        for item in productAffiliate.orderItem.all():
            if item.ordered == True:
                if item.item.discount_price:
                    productAffiliateAmount += item.item.discount_price * item.quantity
                else:
                    productAffiliateAmount += item.item.price * item.quantity
    productAffiliateAmount = round(productAffiliateAmount, 2)

    context={
        'sellerAffiliates': sellerAffiliates,
        "sellerAffiliatesAmount": sellerAffiliatesAmount,
        'productAffiliates': productAffiliates,
        'productAffiliateAmount': productAffiliateAmount
    }
    return render(request, 'affiliate/affiliate-options.html', context)

@login_required
def openAffiliateLink(request, url):
    obj = ProductAffiliate.objects.filter(unique_url=url)
    if len(obj) > 0:
        affiliate = obj[0]
        item = affiliate.item
        addToCart(request, item.slug, False)
        orderItem = OrderItem.objects.get(Q(user=request.user) & Q(
            item__slug=item.slug) & Q(ordered=False))
        affiliate.orderItem.add(orderItem)
        affiliate.save()
        return redirect('product', item.slug)
    else:
        messages.warning(request, 'Invalid URL')
        return redirect('/')

@login_required
def artist_affiliate(request):
    user = get_object_or_404(UserExtended, user=request.user)
    if user.is_refering == False:
        return redirect('register-affiliate')
    return render(request, 'affiliate/artist-affiliate.html')

@login_required
def artwork_affiliate(request):
    user = get_object_or_404(UserExtended, user=request.user)
    if user.is_refering == False:
        return redirect('register-affiliate')
    artworks = ProductAffiliate.objects.filter(user__user=request.user)
    context = {
        'artworks': artworks
    }
    return render(request, 'affiliate/artwork-affiliate.html', context)

@login_required
def add_artwork_affiliate(request):
    if request.method == 'POST':
        try:
            item = request.POST.get('item')
            if ProductAffiliate.objects.filter(item__title=item).exists():
                messages.warning(request, 'Link for this item already exists.')
                return redirect(request.path_info)
            if not Item.objects.filter(title=item).exists():
                messages.warning(request, 'Invalid inputs.')
                return redirect('artwork-affiliate')
            ProductAffiliate.objects.create(
                user = UserExtended.objects.get(user=request.user),
                item = Item.objects.filter(title=item).first()
            )
            messages.success(request, 'Affiliate link created.')
            return redirect('artwork-affiliate')
        except:
            messages.warning(request, 'Invalid inputs.')
            return redirect('artwork-affiliate')
    user = get_object_or_404(UserExtended, user=request.user)
    if user.is_refering == False:
        return redirect('register-affiliate')
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'affiliate/add-artwork-affiliate.html', context)
