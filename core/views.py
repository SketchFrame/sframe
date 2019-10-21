from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from products.models import Item, ItemImages
from django.contrib import messages
from .forms import ContactUsForm
from products.models import Item
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from core.models import FAQ, NewsletterEmails, MainBanner, PrivacyPolicy, AffiliateFAQ

def Verify(request):
    return render(request, 'home/google2afa60e56a73bae5.html')

def back(request):
    return render(request, 'home/back.html')

def login_redirect_view(request):
    return redirect('/')

def home(request):
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
    imgs = [
        'https://images.pexels.com/photos/1572386/pexels-photo-1572386.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',

        'https://images.pexels.com/photos/1585325/pexels-photo-1585325.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',

        'https://images.pexels.com/photos/1209843/pexels-photo-1209843.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',

        'https://images.pexels.com/photos/889839/pexels-photo-889839.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',

        'https://images.pexels.com/photos/1012982/pexels-photo-1012982.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',

        'https://images.pexels.com/photos/2811471/pexels-photo-2811471.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',

        'https://images.pexels.com/photos/1266808/pexels-photo-1266808.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',

        'https://images.pexels.com/photos/1690351/pexels-photo-1690351.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',

        'https://images.pexels.com/photos/1616403/pexels-photo-1616403.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',

        'https://images.pexels.com/photos/1293120/pexels-photo-1293120.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
        
        'https://images.pexels.com/photos/1570779/pexels-photo-1570779.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',

        'https://images.pexels.com/photos/1812960/pexels-photo-1812960.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
    ]
    trendingSearches = [
        'Landscape', 
        'Old age', 
        'Everyday life',
        'Portraits', 
        'Still life', 
        'Street art',  
        'Abstract', 
        'Fantasy', 
        'Fine art', 
        'Pop art', 
        'Mona Lisa', 
        'Semi-abstract', 
        'Figurative',
    ]
    return render(request, 'home/home.html', context={
        'products': l,
        'banners': MainBanner.objects.all()[:3],
        'meta_description': "Choose from the wide variety of art, on demand paintings, sketches and a lot more. Gifts for your love ones, all at a single hub. Easily accessible and affordable.",
        'imgs': imgs,
        'trendingSearches': trendingSearches
    })

def quick_search(request):
    search_text = request.GET.get('q')
    if search_text is not None and search_text != "":
        results = Item.objects.filter(Q(title__icontains = search_text) | Q(title__istartswith = search_text) | Q(title__iendswith = search_text))[:10]
    else:
        results = []
    return render(request, "home/quick-search.html", {'results': results})

def search(request):
    q = request.GET.get('q')
    l = []
    d = {}
    items = Item.objects.filter(Q(title__icontains=q))
    images = ItemImages.objects.all()
    for item in items:
        for image in images:
            if item.slug == image.item.slug:
                d.update({'item': item, 'image': image})
                l.append(d.copy())
                break
            else:
                continue

    return render(request, "home/search.html", {
        'products': l
    })

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['joshirajesh448@gmail.com', ]
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = "Someone from SketchFrame.com"
            contact_no = form.cleaned_data['contact_no']

            complete_message = f"from: {name}\nEmail: {email}\nsubject: {subject}\nmessage: {message}\ncontact number: {contact_no}"
            try:
                send_mail(subject, complete_message,
                          email_from, recipient_list)
                messages.info(request, "Mail sent successfully.")
            except:
                messages.info(request, "Mail was not sent")
                return redirect('contact')
        else:
            messages.info(request, "Form data was invalid")
            return redirect('contact')
    else:
        form = ContactUsForm()
    return render(request, 'home/contact.html', {
        'form': form
    })

def tnc(request):
    return render(request, 'home/tnc.html')

def seller_faq(request):
    questions = FAQ.objects.filter(faq_of='seller')
    return render(request, 'home/seller-faq.html', {'questions': questions})

def user_faq(request):
    questions = FAQ.objects.filter(faq_of='user')
    return render(request, 'home/user-faq.html', {'questions': questions})

def affiliate_faq(request):
    questions = AffiliateFAQ.objects.all()
    return render(request, 'home/affiliate-faq.html', {'questions': questions})

@csrf_exempt
def subscribeToNewsletter(request):
    from django.core.exceptions import ValidationError
    from django.core.validators import EmailValidator

    email = request.POST.get('email')
    validator = EmailValidator()
    try:
        validator(email)
        newsletter, created = NewsletterEmails.objects.get_or_create(email=email)
        if created:
            resp = {
                'message': "Thanks for registering! You will be notified for all the new updates and artworks at SketchFrame.",
                'text': "success"
            }
        else:
            resp = {
                'message': "This email already exists",
                'text': "email-exists",
            }
    except ValidationError:
        resp = {
            'message': 'Error! The email is not correct!',
            'text': "validation-error"
        }
    return JsonResponse(resp)

def privacy(request):
    policies = PrivacyPolicy.objects.all()
    return render(request, 'home/privacy.html', {'policies': policies})
