from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import *

class UserExtended(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)
    mobileNumber = models.CharField(max_length=15, blank=True, null=True)
    orders = models.ManyToManyField('products.Order', blank=True)
    is_refering = models.BooleanField(default=False)
    is_refered = models.BooleanField(default=False)
    paytm_number = models.CharField(max_length=15, blank=True, null=True)
    googlePay_number = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.user.username


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    orderId = models.ForeignKey(
        'products.Order', on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    pincode = models.CharField(max_length=10)
    street_address = models.CharField(max_length=200)
    street_address2 = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    paymentType = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    user = models.ForeignKey('UserExtended', on_delete=models.CASCADE)
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    zipCode = models.CharField(max_length=15)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user.username} Address"

@receiver(post_save, sender=User)
def createUserExtendedModel(instance, created, **kwargs):
    if created:
        UserExtended.objects.create(user=instance)
