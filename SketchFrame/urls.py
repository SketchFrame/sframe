from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from core.views import search, quick_search
from core.views import login_redirect_view
from core.sitemaps import ProductSitemap

sitemaps = {
    'Items': ProductSitemap
}

urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('admin/', include('custom_admin.urls')),
    path('success/url/', login_redirect_view, name='login-redirect'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('user/', include('users.urls')),
    path('seller/', include('seller.urls')),
    path('project/', include('bids.urls')),
    path('shop/', include('shop.urls')),
    path('notifications/', include('notifications.urls')),
    path('search/', search, name="search"),
    path('affiliate/', include('affiliate.urls')),
    path('quick-search/', quick_search, name="quick-search"),
]
