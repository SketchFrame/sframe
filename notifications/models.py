from django.db import models
from users.models import *
from bids.models import *
from seller.models import *
from products.models import *

CATEGORY_CHOICES = (
    ('Alert', 'Alert'),
    ('OrderSuccess', 'OrderSuccess'),
    ('OrderIncomplete', 'OrderIncomplete'),
    ('ProjectAssigned', 'ProjectAssigned'),
    ('ProjectArrived', 'ProjectArrived'),
    ('ProjectCompleted', 'ProjectCompleted'),
    ('BidAdded', 'BidAdded'),
    ('AccountSecurity', 'AccountSecurity'),
    ('PaymentDue', 'PaymentDue'),
    ('PaymentSuccess', 'PaymentSuccess'),
    ('registerdAsSeller', 'registerdAsSeller'),
    ('AddressUpdated', 'AddressUpdated'),
    ('Other', 'Other'),
)


class Notifications(models.Model):
    user = models.ForeignKey('users.UserExtended',
                             on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=120)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=20, default="Other")
    description = models.TextField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    bid = models.ForeignKey(
        'bids.Bids', on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(
        'products.Item', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        'products.Order', on_delete=models.SET_NULL, null=True, blank=True)
    archieve = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


