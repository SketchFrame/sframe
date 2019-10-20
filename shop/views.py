from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from products.models import Item, ItemImages, Order, OrderItem, Comment, Coupon
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.db.models import Q
from django.contrib import messages
from .forms import CheckoutForm, CouponForm, ContactForm, ContactForm2, EditProductComment
from django.utils import timezone
from .PayTm import Checksum
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from users.models import BillingAddress, UserExtended, Address
from django.views.decorators.csrf import csrf_exempt
from affiliate.models import Affiliate
from notifications.models import Notifications
from .render import *
import requests
from threading import Thread, activeCount

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def Pdf(request, pk):
    params = {}
    order = Order.objects.get(pk=pk)
    billing_address = BillingAddress.objects.get(orderId=order)
    
    if order.coupon:
        params.update({
            'coupon': order.coupon,
            'coupon_amount': order.coupon.amount,
        })

    params.update({
        'orderId': pk,
        'fullname' : billing_address.fullname,
        'user' : billing_address.user,
        'phone' : billing_address.phone,
        'email' : billing_address.email,
        'billing_date': order.billing_date,
        'amount': order.amount,
        'pincode' : billing_address.pincode,
        'street_address' : billing_address.street_address,
        'street_address2' : billing_address.street_address2,
        'landmark' : billing_address.landmark,
        'state' : billing_address.state,
        'city' : billing_address.city,
        'items': order.item
    })
    file = Render.render_to_file('shop/pdf.html', params)

    msg = EmailMessage('Order Successful at SketchFrame.com', '<html><b><center><h2>Your order has been successfully placed at SketchFrame.com</h2><p>Please keep the attached invoice.</p><br/>Thank you,<br/>Team SketchFrame.com</center></b></html>',
    settings.EMAIL_HOST_USER, [billing_address.email])
    msg.content_subtype = "html"  
    msg.attach_file(file[1])
    # msg.send()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entries = os.listdir(os.path.join(BASE_DIR, 'invoice'))
    for entry in entries:
        if entry == file[0]:
            os.remove(f"invoice/{file[0]}")
            return 1

@csrf_exempt
def shopView(request):
    l = []
    d = {}
    items = Item.objects.all()
    images = ItemImages.objects.all()
    for item in items:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break
    return render(request, 'shop/home.html', context={
        'products': l,
    })

def productView(request, slug):
    l = []
    d = {}
    thisItem = Item.objects.get(slug=slug)
    if thisItem.approved == False or thisItem.listing_status == False or thisItem.finallySubmitted == False:
        messages.info(request, 'Product is not available.')
        return redirect('shop')
    itemImages = ItemImages.objects.filter(item=thisItem)
    comments = Comment.objects.filter(item=thisItem)

    similarItems = Item.objects.filter(category=thisItem.category)[:3]
    images = ItemImages.objects.all()
    
    for item in similarItems:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break
    
    if request.method == "POST":
        review_msg = request.POST.get("review-msg")
        review_msg = review_msg.replace("'", "\"")
        if review_msg != '':
            rating = int(str(request.POST.get("rating")))
            if rating > 5 or rating < 1:
                messages.warning(request, "Data manipulation detected!")
                return redirect(request.path_info)
            comment = Comment(
                text = review_msg,
                rating = rating
            )
            comment.item = thisItem
            comment.user = get_object_or_404(UserExtended, user=request.user)
            comment.save()
            allComments = Comment.objects.filter(item=thisItem)
            totalRating = 0
            for oneComment in allComments:
                totalRating += oneComment.rating
            newRating = totalRating/len(allComments)
            thisItem.ratings = newRating
            thisItem.save()
            messages.success(request, 'Comment added Successfully.')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, 'Please enter message.')
            return HttpResponseRedirect(request.path_info)
    return render(request, 'shop/product.html', {
        'item': thisItem,
        'itemImages': itemImages,
        'comments': comments,
        'products': l,
    })

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'shop/order_summary.html')

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            addresses = Address.objects.filter(user__user=self.request.user)
            context = {
                'form': form,
                'couponform': CouponForm(),
                'addresses': addresses,
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, 'shop/checkout.html', context)
        except ObjectDoesNotExist:
            # messages.warning(self.request, "You don't have an active order")
            return redirect("order-summary")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = order.get_total()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                orderId = order
                fullname = form.cleaned_data.get('fullname')
                email = self.request.user.email
                address_id = self.request.POST.get('address-value')
                print(address_id)
                address = Address.objects.get(Q(pk=int(address_id)) & Q(user__user=self.request.user))
                payment_type = self.request.POST.get('payment-type')

                billing_address = BillingAddress(
                    user=self.request.user,
                    fullname=fullname,
                    phone=address.phone1,
                    email=email,
                    orderId=orderId,
                    pincode=address.zipCode,
                    street_address=address.address1,
                    street_address2=address.address2,
                    landmark=address.landmark,
                    state=address.state,
                    city=address.city,
                    paymentType=payment_type
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

            
                if self.request.POST.get('payment-type') == 'online':
                    # Redirect to payment gateway
                    param_dict = {
                        'MID': 'WorldP64425807474247',
                        'ORDER_ID': str("SFRAME" + str(orderId.pk)),
                        'TXN_AMOUNT': str(amount),
                        'CUST_ID': address.phone1,
                        'INDUSTRY_TYPE_ID': 'Retail',
                        'WEBSITE': 'WEBSTAGING',
                        'CHANNEL_ID': 'WEB',
                        'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
                        # 'CALLBACK_URL': 'https://sketchframe.herokuapp.com/shop/handlerequest/',
                    }
                    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
                        param_dict, MERCHANT_KEY)
                    return render(self.request, 'shop/paytm.html', {'param_dict': param_dict})
                elif self.request.POST.get('payment-type') == 'offline':
                    
                    order.amount = amount + 50
                    order.billing_date = timezone.now()
                    order.ordered = True
                    order.billing_mode = "Offline"

                    allItems = order.item.all()

                    allItems.update(ordered=True)
                    allItems.update(createdOn=timezone.now())

                    for item in allItems:
                        thisItem = Item.objects.get(pk=item.item.pk)
                        thisItem.stock -= item.quantity
                        thisItem.save()
                        item.save()
                    order.save()
                    
                    # Checking Affiliate.
                    l = []
                    for item in order.item.all():
                        thisItemSeller = item.item.seller
                        affiliate = Affiliate.objects.filter(seller=thisItemSeller.user)
                        if len(affiliate)>0:
                            if affiliate[0].completed == False:
                                affiliate[0].orderItem.add(item)
                                l.append(thisItemSeller.user.user.username)
                                if item.item.discount_price:
                                    itemPrice = item.item.discount_price
                                else:
                                    itemPrice = item.item.price
                                qty = item.quantity
                                price =  (itemPrice/10)*qty
                                affiliate[0].amount += price
                                affiliate[0].save()
                            else:
                                pass
                        else:
                            pass
                    for user in l:
                        affiliate = Affiliate.objects.get(
                            seller__user__username=user)
                        affiliate.completed = True
                        affiliate.save()
                    
                    Pdf(self.request, order.pk)

                    emails = [settings.EMAIL_HOST_USER, ]
                    order = Order.objects.get(pk=order.pk)
                    allItems = order.item.all()
                    for item in allItems:
                        emails.append(item.item.seller.user.user.email)
                        Notifications.objects.create(
                            user=item.item.seller.user,
                            title='Someone ordered your product.',
                            category='OrderSuccess'
                        )

                    msg = EmailMessage('Order Successful at SketchFrame.com',
                                       '<html><b><center><h2>An Order has been placed at SketchFrame.com</h2><p>Please visit your dashboard.</p><br/>https://sketchframe.herokuapp.com/seller/dashboard/<br/>or<br/>http://sketchframe.in/seller/dashboard/</center></b></html>', settings.EMAIL_HOST_USER, emails)
                    msg.content_subtype = "html"
                    # msg.send()

                    return render(self.request, 'shop/paytm-offline.html', {'order': order})
            messages.warning(self.request, "Failed checkout")
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect("order-summary")

@csrf_exempt
def handlerequest(request):
    form = request.POST
    # x = 'Error Code 10'
    respons_dict = {}
    context = {"title": "handlerequest", "response": respons_dict}
    for i in form.keys():
        respons_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
            # = 'Error Code 2'
    verify = Checksum.verify_checksum(respons_dict, MERCHANT_KEY, checksum)
    # print(respons_dict)
    if verify:
        if respons_dict['RESPCODE'] == '01':
            # x = 'Error Code 3'
            # print("Order successful")
            ourVar = form['ORDERID']
            find1 = ourVar.find('SFRAME')
            find2 = ourVar[find1+len('SFRAME'):]
            # findMatch = matches.objects.filter(pk = int(find2)).first()
            findOrder = Order.objects.filter(pk=int(find2)).first()
            order_items = findOrder.item.all()

            order_items.update(ordered=True)
            order_items.update(createdOn=timezone.now())
            for item in order_items:
                thisItem = Item.objects.get(pk=item.item.pk)
                thisItem.stock -= item.quantity
                thisItem.save()
                item.save()

            findOrder.ordered = True
            findOrder.amount = form['TXNAMOUNT']
            findOrder.billing_date = timezone.now()
            findOrder.billing_mode = "Online"
            findOrder.save()

            # Checking Affiliate.
            l = []
            for item in findOrder.item.all():
                thisItemSeller = item.item.seller
                affiliate = Affiliate.objects.filter(
                    seller=thisItemSeller.user)
                if len(affiliate) > 0:
                    if affiliate[0].completed == False:
                        affiliate[0].orderItem.add(item)
                        l.append(thisItemSeller.user.user.username)
                        if item.item.discount_price:
                            itemPrice = item.item.discount_price
                        else:
                            itemPrice = item.item.price
                        qty = item.quantity
                        price = (itemPrice/10)*qty
                        affiliate[0].amount += price
                        affiliate[0].save()
                    else:
                        pass
                else:
                    pass
            for user in l:
                affiliate = Affiliate.objects.get(
                    seller__user__username=user)
                affiliate.completed = True
                affiliate.save()

            findAddress = BillingAddress.objects.filter(orderId=find2).first()
            fullname = findAddress.fullname
            user = findAddress.user
            phone = findAddress.phone
            email = findAddress.email
            pincode = findAddress.pincode
            street_address = findAddress.street_address
            street_address2 = findAddress.street_address2
            landmark = findAddress.landmark
            state = findAddress.state
            city = findAddress.city
            amount = form['TXNAMOUNT']

            Pdf(request, find2)

            context.update({'fullname': fullname, 'amount': amount, 'user': user, 'phone': phone, 'pincode': pincode, 'street_address': street_address,
                            'street_address2': street_address2, 'landmark': landmark, 'state': state, 'city': city, 'email': email})
            
            emails = [settings.EMAIL_HOST_USER, ]
            order = Order.objects.get(pk=find2)
            allItems = order.item.all()
            for item in allItems:
                emails.append(item.item.seller.user.user.email)
                Notifications.objects.create(
                    user=item.item.seller.user,
                    title='Someone ordered your product.',
                    category='OrderSuccess'
                )

            msg = EmailMessage('Order Successful at SketchFrame.com',
                               '<html><b><center><h2>An Order has been placed at SketchFrame.com</h2><p>Please visit your dashboard.</p><br/>https://sketchframe.herokuapp.com/seller/dashboard/<br/>or<br/>http://sketchframe.in/seller/dashboard/</center></b></html>', settings.EMAIL_HOST_USER, emails)
            msg.content_subtype = "html"
            # msg.send()
        else:
            print("Order was not successful because " +
                  respons_dict['RESPMSG'])

            ourVar = form['ORDERID']
            find1 = ourVar.find('SFRAME')
            find2 = ourVar[find1+len('SFRAME'):]
            findOrder = Order.objects.filter(pk=int(find2)).first()
            findOrder.delete()
    else:
        print("order unsuccessful because"+respons_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', context)

@login_required
def addToCart(request, slug, showMsg=True):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            if showMsg:
                messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.item.add(order_item)
            if showMsg:
                messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        if showMsg:
            messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")

@login_required
def removeFromCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                # order.item.remove(order_item)
                order_item.delete()
                order_qs = Order.objects.filter(
                    user=request.user, ordered=False).first()
                if order_qs.item.count() == 0:
                    order_qs.delete()
                    messages.info(request, "Item was removed from your cart.")
                    return redirect("shop")
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
    return redirect("shop", slug=slug)

@login_required
def deleteFromCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # order.item.remove(order_item)
            order_item.delete()
            order_qs = Order.objects.filter(
                user=request.user, ordered=False).first()
            if order_qs.item.count() == 0:
                order_qs.delete()
                messages.info(request, "Item was removed from your cart.")
                return redirect("shop")
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("shop", slug=slug)
    else:
        #  Add a message saying, user dosen't have order
        messages.info(request, "You do not have an active order.")
        return redirect("shop", slug=slug)

@login_required
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        return 101

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                couponCode = get_coupon(self.request, code)
                if couponCode == 101:
                    return render(self.request, "shop/coupon-message.html")
                if couponCode.amount > order.get_total():
                    return render(self.request, "shop/coupon-message.html", {'error': True})
                order.coupon = couponCode
                order.save()
                return render(self.request, "shop/coupon-message.html", {'order': order})
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")

@login_required
def EditCommentView(request, pk):
    comment = Comment.objects.filter(Q(pk=pk) & Q(user__user=request.user))
    if comment.exists():
        if request.method == 'POST':
            form = EditProductComment(request.POST)
            if form.is_valid():
                rating = int(str(request.POST.get('rating')))
                if rating == '':
                    rating = comment[0].rating
                if rating > 5 or rating < 1:
                    messages.warning("Data manipulation detected! Please enter valid data")
                    return redirect(request.path_info)
                text = request.POST.get('text')
                initialComments = Comment.objects.filter(item=comment[0].item)
                totalRating = 0
                for oneComment in initialComments:
                    if oneComment.pk == pk:
                        continue
                    totalRating += oneComment.rating
                newRating = (totalRating + rating)/len(initialComments)
                comment.update(
                    text=text,
                    edited_date=timezone.now(),
                    rating=int(rating)
                )
                item = Item.objects.get(slug=comment[0].item.slug)
                item.ratings = newRating
                item.save()
                messages.success(request, "Comment Updated")
                return redirect('product', slug=comment[0].item.slug)
            else:
                messages.warning(request, "Form is Invalid")
                return redirect(request.path_info)
        else:
            form = EditProductComment(initial={
                'text': comment[0].text,
            })
    else:
        messages.warning(request, "Comment does not exists")
        return redirect('/')
    return render(request, "shop/edit-comments.html", {
        'form': form,
        'rating': comment[0].rating,
        'text': comment[0].text
    })

def trendingProducts(request):
    l = []
    d = {}
    items = Item.objects.all()
    images = ItemImages.objects.all()
    for item in items:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break
    return render(request, "shop/product-tabs.html", {
        'products': l
    })

def bestSeller(request):
    l = []
    d = {}
    items = Item.objects.all()
    images = ItemImages.objects.all()
    for item in items:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break
    return render(request, "shop/product-tabs.html", {
        'products': l
    })

def latestArtwork(request):
    l = []
    d = {}
    items = Item.objects.all()
    images = ItemImages.objects.all()
    for item in items:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break
    return render(request, "shop/product-tabs.html", {
        'products': l
    })

@csrf_exempt
def quickView(request):
    slug = request.POST.get('slug')
    print(slug)
    item = Item.objects.get(slug=slug)
    images = ItemImages.objects.filter(item=item)
    comments = Comment.objects.filter(item=item)
    return render(request, "shop/quick-view.html", {"item": item, "images": images, "comments": comments})
