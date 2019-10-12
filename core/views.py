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
        'https://miro.medium.com/proxy/1*2uRQQyR92M6PUKJRH81U_w.jpeg',
        'https://cdn.eventfinda.co.nz/uploads/events/transformed/1246598-555064-34.jpg?v=2',
        'https://render.fineartamerica.com/images/rendered/default/print/10.000/8.375/break/images-medium-5/fledglings-anna-bain.jpg',
        'https://d3nn873nee648n.cloudfront.net/HomeImages/Without-People.jpg',
        'http://www.lacma.org/sites/default/files/styles/exhibition_image/public/primary_image/2018-11/AC1992_136_1-20140414.jpg?itok=7ibfPJPQ',
        'https://www.washingtonian.com/wp-content/uploads/2019/07/BR2603-2048x2698.jpg',
        'https://i.pinimg.com/originals/a5/b3/4a/a5b34ac8665dd7945d95698662232c9b.jpg',
        'https://i.pinimg.com/originals/a3/18/c7/a318c734f63664e3f42d61792ddeeaeb.jpg',
        'https://d3nn873nee648n.cloudfront.net/HomeImages/Lifestyle-Families.jpg',
        'https://d3nn873nee648n.cloudfront.net/HomeImages/Vacation-and-Holidays.jpg',
        'https://d3nn873nee648n.cloudfront.net/HomeImages/Without-People.jpg',
    ]
    return render(request, 'home/home.html', context={
        'products': l,
        'banners': MainBanner.objects.all()[:3],
        'meta_description': "Choose from the wide variety of art, on demand paintings, sketches and a lot more. Gifts for your love ones, all at a single hub. Easily accessible and affordable.",
        'imgs': imgs
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
