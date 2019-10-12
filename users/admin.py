from django.contrib import admin
from .models import UserExtended, BillingAddress, Address

admin.site.register(UserExtended)
admin.site.register(BillingAddress)
admin.site.register(Address)
