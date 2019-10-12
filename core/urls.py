from django.urls import path
from .views import(
    home,
    about,
    contact,
    tnc,
    privacy,
    Verify,
    back,
    seller_faq,
    user_faq,
    affiliate_faq,
    subscribeToNewsletter
)

urlpatterns = [
    path('', home, name="home"),
    path('back/', back, name="back"),
    path('google2afa60e56a73bae5.html', Verify, name="Verify"),
    path('about/', about, name="about"),
    path('seller-faq/', seller_faq, name="seller-faq"),
    path('user-faq/', user_faq, name="user-faq"),
    path('affiliate-faq/', affiliate_faq, name="affiliate-faq"),
    path('contact/', contact, name="contact"),
    path('terms-and-conditions/', tnc, name="tnc"),
    path('privacy/', privacy, name="privacy"),
    path('subscribe-to-newsletter/', subscribeToNewsletter, name="subscribe-newsletter"),
]
