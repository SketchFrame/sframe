from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'ordered']

admin.site.register(Item)
admin.site.register(OrderItem, OrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon)
admin.site.register(ItemImages)
admin.site.register(Comment)
admin.site.register(PackageInformation) 
