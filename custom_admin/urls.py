from django.urls import path
from .views import (
    admin_dashboard, 
    refresh_charges
    )

urlpatterns = [
    path('', admin_dashboard, name='admin-dashboard'),
    path('refresh-charges/', refresh_charges, name='refresh-charges'),
]
