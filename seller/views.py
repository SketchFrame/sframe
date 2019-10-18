from django.views.generic import UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from users.models import UserExtended
from products.models import Item, ItemImages, OrderItem
from notifications.models import Notifications
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from bids.models import project, Bids
from .decorators import seller_required
from django.utils import timezone
from seller.models import Seller, SellerAddress, SellerExtended, SellerComment, PortfolioImages
from django.http import HttpResponseRedirect
from affiliate.models import Affiliate
from django.db.models import Q
import datetime
from django.core.exceptions import ObjectDoesNotExist

def viewSellerProfile(request, username):
    seller = Seller.objects.get(user__user__username=username)
    if request.method == "POST":
        review_msg = request.POST.get("review-msg")
        review_msg = review_msg.replace("'", "\"")
        rating = str(request.POST.get("rating"))
        if rating == '':
            messages.warning(request, "Please Give a rating")
            return redirect(request.path_info)
        rating = int(rating)
        if rating > 5 or rating < 1:
            messages.warning("Data manipulation detected! Please enter valid data")
            return redirect(request.path_info)
        user = UserExtended.objects.get(user=request.user)
        if review_msg != '':
            comment = SellerComment(
                text=review_msg,
                rating=int(rating)
            )
            comment.seller = seller
            comment.user = user
            comment.save()
            allComments = SellerComment.objects.filter(seller=seller)
            thisSeller = SellerExtended.objects.get(seller=seller)
            totalRating = 0
            for oneComment in allComments:
                totalRating += oneComment.rating
            newRating = totalRating/len(allComments)
            thisSeller.rating = newRating
            thisSeller.save()
            Notifications.objects.create(
                user=seller.user,
                title="You have a new comment on your profile",
                category="Other"
            )
            messages.success(request, 'Comment added Successfully.')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, 'Please enter message.')
            return HttpResponseRedirect(request.path_info)

    sellerAddress = SellerAddress.objects.get(seller=seller)
    sellerExtended = SellerExtended.objects.get(seller=seller)
    portfolioImages = PortfolioImages.objects.filter(seller=seller)
    sellerComment = SellerComment.objects.filter(seller=seller)
    products = Item.objects.filter(seller=seller)

    l = []
    d = {}
    images = ItemImages.objects.filter(item__seller=seller)
    for item in products:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break

    return render(request, 'home/profile.html', {
        'seller': seller,
        'sellerAddress': sellerAddress,
        'sellerExtended': sellerExtended,
        'sellerComment': sellerComment,
        'portfolioImages': portfolioImages,
        'products': l
    })

@login_required
def editComment(request, pk):
    comment = SellerComment.objects.filter(pk=pk)
    if comment.exists():
        if request.method == 'POST':
            form = EditCommentsForm(request.POST)
            if form.is_valid():
                rating = str(request.POST.get('rating'))
                if rating == '':
                    rating = comment[0].rating
                rating = int(rating)
                if rating > 5 or rating < 1:
                    messages.warning("Data manipulation detected! Please enter valid data")
                    return redirect(request.path_info)
                text = form.cleaned_data['text']
                initialComments = SellerComment.objects.filter(seller=comment[0].seller)
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
                seller = SellerExtended.objects.get(seller=comment[0].seller)
                seller.rating = newRating
                seller.save()
                messages.success(request, "Comment Updated")
                return redirect('view-seller-profile', username=comment[0].seller.user.user.username)
            else:
                messages.warning(request, "Form is Invalid")
                return redirect(request.path_info)
        else:
            form = EditCommentsForm(initial={
                'text': comment[0].text,
            })
    else:
        messages.warning(request, "Comment does not exists")
        return redirect('/')
    return render(request, "home/update-comment.html", {
        'form': form,
        'rating': comment[0].rating,
    })

@login_required
@seller_required
def myShop(request):
    seller = get_object_or_404(
        Seller, user__user__username=request.user.username)
    if seller.basic_profile_completed == False:
        messages.info(request, "Complete your profile first.")
        return redirect('complete-profile')
    l = []
    d = {}
    published_items = 0
    total_sale = 0
    total_income = 0
    total_sale_this_month = 0
    total_income_this_month = 0
    # try:
    items = Item.objects.filter(
        seller__user__user=request.user)[:3]
    images = ItemImages.objects.filter(
        item__seller__user__user=request.user)
    for item in items:
        if item.listing_status:
            published_items += 1
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break
            
    orderItems = OrderItem.objects.filter(Q(ordered=True) & Q(item__seller__user__user = request.user))
    for orderItem in orderItems:
        if orderItem.createdOn:
            if (datetime.datetime.now().year == orderItem.createdOn.year) and (datetime.datetime.now().month == orderItem.createdOn.month):
                if orderItem.item.discount_price:
                    total_income_this_month += orderItem.item.originalDiscount_price * orderItem.quantity
                else:
                    total_income_this_month += orderItem.item.originalPrice * orderItem.quantity
                total_sale_this_month += orderItem.quantity

        if orderItem.item.discount_price:
            total_income += orderItem.item.originalDiscount_price * orderItem.quantity
        else: 
            total_income += orderItem.item.originalPrice * orderItem.quantity
        total_sale += orderItem.quantity
    context = {
        'products': l,
        'total_sale': total_sale,
        'total_income': total_income,
        'total_sale_this_month': total_sale_this_month,
        'total_income_this_month': total_income_this_month,
        'total_products': Item.objects.filter(seller__user__user=request.user).count(),
        'published_items': Item.objects.filter(Q(seller__user__user=request.user) & Q(listing_status=True)).count()
    }
    return render(request, 'seller/home.html', context)

@login_required
@seller_required
def projectAssigned(request):
    bids = Bids.objects.filter(user__user__user=request.user)
    try:
        notification = Notifications.objects.get(
            Q(user__user=request.user) & Q(bid__project__assignedTo__user=request.user))
        notification.viewed = True
        notification.save()
    except:
        pass
    completed = project.objects.filter(
        Q(assignedTo__user=request.user) & Q(is_completed=True))
    active = project.objects.filter(
        Q(assignedTo__user=request.user) & Q(is_completed=False))
    context = {
        'completed': completed,
        'active': active,
        'bids': bids,
    }
    return render(request, 'seller/project-assigned.html', context)

@login_required
@seller_required
def completed(request, slug):
    projectName = get_object_or_404(project, Q(
        slug=slug) & Q(assignedTo__user=request.user))
    projectName.is_completed = True
    projectName.completedOn = timezone.now()
    Notifications.objects.create(
        category="ProjectCompleted",
        user=projectName.user,
        title=f"{request.user.username} has completed your project {projectName.title}"
    )
    projectName.save()
    messages.success(request, "Notification sent to client")
    return redirect('project-assigned')

@login_required
def register(request):
    user = get_object_or_404(
        UserExtended, user__username=request.user.username)
    if request.method == 'POST':
        if request.POST.get('code'):
            if request.POST.get('code') == request.user.username:
                messages.warning(request, "Invalid Code.")
                return HttpResponseRedirect(request.path_info)
            if len(User.objects.filter(username = request.POST.get('code'))) == 0:
                messages.warning(request, "Invalid Code.")
                return HttpResponseRedirect(request.path_info)
            user.is_refered = True
            Affiliate.objects.create(
                seller = UserExtended.objects.get(user=request.user),
                user=UserExtended.objects.get(user__username = request.POST.get('code'))
            )
        user.is_seller = True
        user.save()
        Seller.objects.create(user=user)
        messages.success(request, "Successfully registered as a Seller.")
        Notifications.objects.create(
            user=user,
            title="Congratulations! You are now a seller.",
            category="registerdAsSeller",
            description=f"{request.user.username} Thank you for becoming a part of SketchFrame Seller community. Now, you can browse as well as post projects or you can add them by yourself too.You can visit your profile at <a href='#' class='text-info'>sketchframe.com/seller/profile/f{request.user.username}</a> and your dashboard is available at <a href='#'>sketchframe.com/seller/dashboard/</a> to get started with our polcies, terms and conditions visit our <a href='#' class='text-info'>Help center.</a>"
        )
        return redirect('complete-profile')
    if user.is_seller == True:
        seller = get_object_or_404(
            Seller, user__user__username=request.user.username)
        sellerAddress = get_object_or_404(
            SellerAddress, seller=seller
        )
        sellerExtended = get_object_or_404(
            SellerExtended, seller=seller
        )
        if seller.basic_profile_completed == False:
            messages.info(request, "Complete your profile first.")
            return redirect('complete-profile')
        if sellerAddress.address_profile_completed == False:
            messages.info(request, "Please Give your Address")
            return redirect('complete-profile')
        if sellerExtended.description_profile_completed == False:
            messages.info(request, "Please enter your Bio")
            return redirect('complete-profile')
        return redirect('complete-profile')

    return render(request, 'seller/register.html')

@login_required
@seller_required
def complete_profile(request):
    if request.method == 'POST':
        address_form = SellerAddressForm(request.POST)
        info_form = SellerDetialsForm(request.POST)
        extended_form = SellerExtendedForm(request.POST)
        images_form = SellerImages(request.POST or None, request.FILES or None)

        if address_form.is_valid() and info_form.is_valid() and extended_form.is_valid():
            s = get_object_or_404(Seller, user__user=request.user)
            s.fname = info_form.cleaned_data['fname']
            s.lname = info_form.cleaned_data['lname']
            s.gstNumber = info_form.cleaned_data['gstNumber']
            s.speciality = info_form.cleaned_data['speciality']
            s.experience = info_form.cleaned_data['experience']
            s.gender = info_form.cleaned_data['gender']
            s.basic_profile_completed = True
            s.save()
            if images_form.is_valid():
                s.profile_img = images_form.cleaned_data['profile_img']
                s.cover_img = images_form.cleaned_data['cover_img']
                s.save()
            address = SellerAddress(
                seller=s,
                zipCode=address_form.cleaned_data['zipCode'],
                city=address_form.cleaned_data['city'],
                state=address_form.cleaned_data['state'],
                country=address_form.cleaned_data['country'],
                address_profile_completed=True
            )
            address.save()
            extended = SellerExtended(
                seller=s,
                bio=extended_form.cleaned_data['bio'],
                facebook=extended_form.cleaned_data['facebook'],
                instagram=extended_form.cleaned_data['instagram'],
                youtube=extended_form.cleaned_data['youtube'],
                twitter=extended_form.cleaned_data['twitter'],
                linkedin=extended_form.cleaned_data['linkedin'],
                Pencil_work=extended_form.cleaned_data['Pencil_work'],
                Pastel_colours=extended_form.cleaned_data['Pastel_colours'],
                Water_colours=extended_form.cleaned_data['Water_colours'],
                Acrylic_colours=extended_form.cleaned_data['Acrylic_colours'],
                Fabric_colours=extended_form.cleaned_data['Fabric_colours'],
                Oil_colours=extended_form.cleaned_data['Oil_colours'],
                Mix_media=extended_form.cleaned_data['Mix_media'],
                description_profile_completed=True,
            )
            extended.save()
            Notifications.objects.create(
                user=get_object_or_404(UserExtended, user=request.user),
                title="Profile Updated!",
                category="AddressUpdated",
            )
            return redirect("seller-profile")
            return redirect(request.path_info)
        else:
            messages.info(request, "Invalid Information")
            return redirect('complete-profile')
    else:
        seller = get_object_or_404(
            Seller, user__user__username=request.user.username)
        if seller.basic_profile_completed == True:
            return redirect('seller-profile')
        address_form = SellerAddressForm()
        info_form = SellerDetialsForm()
        images_form = SellerImages()
        extended_form = SellerExtendedForm()

    return render(request, 'seller/complete-profile.html', {
        'address_form': address_form,
        'info_form': info_form,
        'extended_form': extended_form,
        'images_form': images_form,
    })

@login_required
@seller_required
def seller_profile(request):
    userExtended = get_object_or_404(
        UserExtended, Q(user=request.user) & Q(is_seller=True))
    seller = Seller.objects.get(user=userExtended)
    sellerExtended = SellerExtended.objects.get(seller=seller)
    portfolioImages = PortfolioImages.objects.filter(seller=seller)
    sellerComment = SellerComment.objects.filter(seller=seller)
    products = Item.objects.filter(seller=seller)

    l = []
    d = {}
    images = ItemImages.objects.filter(item__seller=seller)
    for item in products:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break

    return render(request, 'seller/profile.html', {
        'userExtended': userExtended,
        'seller': seller,
        'sellerExtended': sellerExtended,
        'portfolioImages': portfolioImages,
        'sellerComment': sellerComment,
        'products': l
    })

@login_required
@seller_required
def SellerPortfolio(request):
    if request.method == "POST":
        form = PortfolioImagesForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.seller = get_object_or_404(
                Seller, user__user__username=request.user.username)
            portfolio.save()
            messages.success(request, f"Uploaded Image")
            return redirect('seller-profile')
        else:
            messages.warning(request, f"Invalid data")
            return redirect('seller-profile')
    else:
        form = PortfolioImagesForm()
    return render(request, "seller/upload-portfolio-images.html", {
        'form': form
    })

@method_decorator([login_required, seller_required], name="dispatch")
class DeletePortfolioImage(DeleteView):
    model = PortfolioImages
    template_name = "seller/delete-portfolio-images.html"
    success_url = "/seller/profile"

@login_required
@seller_required
def editBio(request):
    seller = Seller.objects.get(user__user=request.user)
    extended = SellerExtended.objects.get(seller=seller)

    if request.method == "POST":
        form = EditBioForm(request.POST)
        if form.is_valid():
            extended.bio = form.cleaned_data['bio']
            extended.save()
            return redirect('seller-profile')
        else:
            messages.warning(request, "Data is invalid")
    else:
        form = EditBioForm(initial={
            'bio': extended.bio
        })
    return render(request, "seller/edit-profile.html", {
        'edit': 'Change your Bio',
        'form': form
    })

@login_required
@seller_required
def editSkills(request):
    seller = Seller.objects.get(user__user=request.user)
    extended = SellerExtended.objects.get(seller=seller)

    if request.method == "POST":
        form = EditSkillsForm(request.POST)
        if form.is_valid():
            extended.Pencil_work = form.cleaned_data['Pencil_work']
            extended.Pastel_colours = form.cleaned_data['Pastel_colours']
            extended.Water_colours = form.cleaned_data['Water_colours']
            extended.Acrylic_colours = form.cleaned_data['Acrylic_colours']
            extended.Fabric_colours = form.cleaned_data['Fabric_colours']
            extended.Oil_colours = form.cleaned_data['Oil_colours']
            extended.Mix_media = form.cleaned_data['Mix_media']
            extended.save()
            return redirect('seller-profile')
        else:
            messages.warning(request, "Data is invalid")
    else:
        form = EditSkillsForm(initial={
            'Pencil_work': extended.Pencil_work,
            'Pastel_colours': extended.Pastel_colours,
            'Water_colours': extended.Water_colours,
            'Acrylic_colours': extended.Acrylic_colours,
            'Fabric_colours': extended.Fabric_colours,
            'Oil_colours': extended.Oil_colours,
            'Mix_media': extended.Mix_media,
        })
    return render(request, "seller/edit-profile.html", {
        'edit': 'Add More',
        'form': form
    })

@login_required
@seller_required
def editSocialInfo(request):
    seller = Seller.objects.get(user__user=request.user)
    extended = SellerExtended.objects.get(seller=seller)

    if request.method == "POST":
        form = EditSocialInfoForm(request.POST)
        if form.is_valid():
            extended.facebook = form.cleaned_data['facebook']
            extended.instagram = form.cleaned_data['instagram']
            extended.youtube = form.cleaned_data['youtube']
            extended.twitter = form.cleaned_data['twitter']
            extended.linkedin = form.cleaned_data['linkedin']
            extended.save()
            return redirect('seller-profile')
        else:
            messages.warning(request, "Data is invalid")
    else:
        form = EditSocialInfoForm(initial={
            'facebook':extended.facebook,
            'instagram':extended.instagram,
            'youtube':extended.youtube,
            'twitter':extended.twitter,
            'linkedin':extended.linkedin 
        })
    return render(request, "seller/edit-profile.html", {
        'edit': 'Change your social media presence',
        'form': form
    })

@login_required
@seller_required
def payments(request):
    return render(request, "seller/payments.html")

@login_required
@seller_required
def AddBankDetails(request):
    if request.method == "POST":
        form = AddBankDetails(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.seller = Seller.objects.get(user__user=request.user)
            bank.save()
            messages.success(request, "Added bank details")
            return redirect(request.path_info)
    else:
        form = AddBankDetailsForm()
    return render(request, "seller/payments.html", {
        'form': form
    })
