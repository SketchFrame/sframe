from django.urls import path
from .views import (
    shopView,
    productView,
    addToCart,
    removeFromCart,
    deleteFromCart,
    OrderSummaryView,
    CheckoutView,
    handlerequest,
    AddCouponView,
    EditCommentView,
    trendingProducts,
    bestSeller,
    latestArtwork,
    quickView
)

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('handlerequest/', handlerequest, name='handlerequest'),
    path('cart/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug:slug>/', addToCart, name="add-to-cart"),
    path('remove-from-cart/<slug:slug>/',
         removeFromCart, name="remove-from-cart"),
    path('delete-from-cart/<slug:slug>/',
         deleteFromCart, name="delete-from-cart"),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('edit-comment/<int:pk>/', EditCommentView, name="edit-comment-product"),
    path('quick-view/', quickView, name="quick-view"),
    path('trending/', trendingProducts, name="trending-products"),
    path('best-sellers/', bestSeller, name="best-sellers"),
    path('latest/', latestArtwork, name="latest-artwork"),
    path('<slug:slug>/', productView, name="product"),
    path('', shopView, name='shop'),
]