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
)
from products.views import (
    addProductStep1,
    addProductStep2,
    viewProduct,
    ProductUpdateView,
    ProductImagesUpdate,
    ProductDeleteView,
    viewAllProduct,
    get_charges,
    uploadImages
)

urlpatterns = [
    path('add-product/', addProductStep1, name="add-product-step1"),
    path('add-product/<slug:slug>/step2/',
         addProductStep2, name="add-product-step2"),
    path('view-product/', viewAllProduct, name="view-all-product"),
    path('view-product/<slug:slug>/', viewProduct, name="view-product"),
    path('edit-product/<slug:slug>/',
         ProductUpdateView.as_view(), name="edit-product"),
    path('edit/<slug:slug>/images/', ProductImagesUpdate,
         name="edit-product-images/"),
    path('delete-product/<slug:slug>/',
         ProductDeleteView.as_view(), name="delete-product"),
    path('dashboard/', myShop, name='my-shop'),
    path('register/', register, name='register-seller'),
    path('complete-profile/', complete_profile, name='complete-profile'),
    path('profile/', seller_profile, name='seller-profile'),
    path('portfolio/upload/', SellerPortfolio, name='portfolio-upload'),
    path('portfolio/delete/<int:pk>/',
         DeletePortfolioImage.as_view(), name="portfolio-delete"),
    path('project-assigned/', projectAssigned, name='project-assigned'),
    path('project-completed/<slug:slug>/', completed, name='project-completed'),
    path('add/product/image/<slug:slug>/', uploadImages, name="add-images"),
    path('edit/comment/<int:pk>/', editComment, name="edit-comment"),
    path('edit/bio/', editBio, name="edit-bio"),
    path('edit/skills/', editSkills, name="edit-skills"),
    path('edit/social/', editSocialInfo, name="edit-social"),
    path('get-charges/', get_charges, name="get-charges"),
    path('<str:username>/', viewSellerProfile, name="view-seller-profile"),
]
