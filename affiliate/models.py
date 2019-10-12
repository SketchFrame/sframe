from django.db import models
from users.models import *
from seller.models import *
from products.models import *
import random
import string


def randomStringDigits(stringLength=6):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

class Affiliate(models.Model):
    user = models.ForeignKey('users.UserExtended', on_delete=models.CASCADE, related_name="affiliate_user", blank=True, null=True)
    seller = models.ForeignKey(
        'users.UserExtended', on_delete=models.CASCADE, related_name="affiliate_seller", blank=True, null=True)
    completed = models.BooleanField(default=False) 
    amount = models.FloatField(default=0)
    orderItem = models.ManyToManyField(
        'products.OrderItem', blank=True, related_name="affiliate_item_list")
    date = models.DateTimeField(auto_now_add=True)
    isPaid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user.username} to {self.seller.user.username}"

class ProductAffiliate(models.Model):
    unique_url = models.CharField(max_length=20, blank=True, null=True, unique=True)
    user = models.ForeignKey(
        'users.UserExtended', on_delete=models.CASCADE, related_name="product_affiliate_user", blank=True, null=True)
    item = models.ForeignKey(
        'products.Item', on_delete=models.CASCADE, null=True)
    orderItem = models.ManyToManyField(
        'products.OrderItem', blank=True, related_name="affiliate_product")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username}'s, {len(self.orderItem.all())} of {self.item.title}"

    def save(self, *args, **kwargs):
        if not self.unique_url:
            self.unique_url = self._get_unique_url()
        super().save(*args, **kwargs)

    def _get_unique_url(self):
        slug = randomStringDigits()
        unique_slug = slug
        num = 1
        while ProductAffiliate.objects.filter(unique_url=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        url = unique_slug
        return url

