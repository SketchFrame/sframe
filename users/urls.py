from django.urls import path
from .views import(
    profile,
    addAddress,
    editAddress,
    delAddress
)

urlpatterns = [
    path('profile/', profile, name='account_profile'),
    path('add-address/', addAddress, name="add-address"),
    path('edit-address/<int:pk>/', editAddress, name="edit-address"),
    path('delete-address/<int:pk>/', delAddress, name="del-address"),
]
