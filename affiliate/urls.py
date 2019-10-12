from django.urls import path
from .views import (
    register,
    artist_affiliate,
    artwork_affiliate,
    openAffiliateLink,
    affiliate_options,
    add_artwork_affiliate
)


urlpatterns = [
    path('', register, name='register-affiliate'),
    path('artist-affiliate/', artist_affiliate, name='artist-affiliate'),
    path('artwork-affiliate/', artwork_affiliate, name='artwork-affiliate'),
    path('add-artwork-affiliate/', add_artwork_affiliate, name='add-artwork-affiliate'),
    path('options/', affiliate_options, name='affiliate-options'),
    path('<str:url>/', openAffiliateLink, name='open-affiliate-link')
]
