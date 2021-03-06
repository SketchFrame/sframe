from django.urls import path
from .views import(
    register,
    complete_profile,
    seller_profile,
    myShop,
    projectAssigned,
    completed,
    viewSellerProfile,
    editComment,
    SellerPortfolio,
    DeletePortfolioImage,
    editBio,
    editSkills,
    editSocialInfo,
    seller_settings,
    generalProfileSettings,
    payments
)
from products.views import (
    addProductStep1,
    addProductStep2,
    viewProduct,
    ProductDeleteView,
    viewAllProduct,
    get_charges,
    uploadImages,
    my_orders,
)

urlpatterns = [
    path('settings/', seller_settings, name="seller-settings"),
    path('product/', addProductStep1, name="add-product-step1"),
    path('product/<slug:slug>/', addProductStep2, name="edit-product"),
    path('settings/edit/', generalProfileSettings, name="general-settings"),
    path('view-product/', viewAllProduct, name="view-all-product"),
    path('view-product/<slug:slug>/', viewProduct, name="view-product"),    
    path('delete-product/<slug:slug>/', ProductDeleteView.as_view(), name="delete-product"),
    path('dashboard/', myShop, name='my-shop'),
    path('dashboard/my-orders/', my_orders, name='my-orders'),
    path('dashboard/payments/', payments, name='payments'),
    path('register/', register, name='register-seller'),
    path('complete-profile/', complete_profile, name='complete-profile'),
    path('profile/', seller_profile, name='seller-profile'),
    path('portfolio/upload/', SellerPortfolio, name='portfolio-upload'),
    path('portfolio/delete/<int:pk>/', DeletePortfolioImage.as_view(), name="portfolio-delete"),
    path('project-assigned/', projectAssigned, name='project-assigned'),
    path('project-completed/<slug:slug>/', completed, name='project-completed'),
    path('add/product/image/<slug:slug>/<int:number>', uploadImages, name="add-images"),
    path('edit/comment/<int:pk>/', editComment, name="edit-comment"),
    path('edit/bio/', editBio, name="edit-bio"),
    path('edit/skills/', editSkills, name="edit-skills"),
    path('edit/social/', editSocialInfo, name="edit-social"),
    path('get-charges/', get_charges, name="get-charges"),
    path('<str:username>/', viewSellerProfile, name="view-seller-profile"),
]
