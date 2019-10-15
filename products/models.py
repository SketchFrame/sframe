from django.conf import settings
from django.db import models
from seller.models import *
from django.utils.text import slugify
from django.shortcuts import reverse
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_delete
from ckeditor.fields import RichTextField
from users.models import *
from django.utils import timezone
from core.models import *
from sorl.thumbnail import ImageField
import uuid


CATEGORY_CHOICES = (
    ('Pencil work', 'Pencil work'),
    ('Pastel colours', 'Pastel colours'),
    ('Water colours', 'Water colours'),
    ('Acrylic colours', 'Acrylic colours'),
    ('Fabric colours', 'Fabric colours'),
    ('Oil colours', 'Oil colours'),
    ('Mix media', 'Mix Media'),
)

SUB_CATEGORY_CHOICES = (
    ('Abstract', 'Abstract'),
    ('Conceptual', 'Conceptual'),
    ('Digital Age', 'Digital Age'),
    ('Everyday Life', 'Everyday Life'),
    ('Fantasy' , 'Fantasy'),
    ('Fashion', 'Fashion'),
    ('Figurative', 'Figurative'),
    ('Fine Art','Fine Art'),
    ('Historical and Political', 'Historical and Political'),
    ('Landscape', 'Landscape'),
    ('Marine', 'Marine'),
    ('Nature', 'Nature'),
    ('Nude', 'Nude'),
    ('Pop Culture', 'Pop Culture'),
    ('Portrait', 'Portrait'),
    ('Provocative', 'Provocative'),
    ('Religion', 'Religion'),
    ('Self Portrait', 'Self Portrait'),
    ('Still Life', 'Still Life'),
    ('Street Art', 'Street Art'),
    ('Urban', 'Urban'),
    ('Vanitas', 'Vanitas'),
    ('Other', 'Other')
)

class Item(models.Model):
    seller = models.ForeignKey(
        'seller.Seller', on_delete=models.CASCADE, null=True, related_name='item_by')
    title = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=20, blank=True, null=True)
    subCategory = models.CharField(
        choices=SUB_CATEGORY_CHOICES, blank=True, null=True, default="Other", max_length=50)
    
    originalPrice = models.FloatField(blank=True, null=True)
    gst = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)
    
    fullDescription = RichTextField(blank=True, null=True)
    shortDescription = models.CharField(max_length=150, blank=True, null=True)
    
    dispatch_time = models.IntegerField(default=0)
    ratings = models.FloatField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    listing_status = models.BooleanField(default=False)
    
    approved = models.BooleanField(default=False)
    
    height = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    stock = models.IntegerField(default=1)
    
    sku = models.CharField(max_length=50, blank=True, null=True)
    hsnCode = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    
    addFrame = models.BooleanField(default=False)
    frameCost = models.FloatField(blank=True, null=True)

    finallySubmitted = models.BooleanField(default=False)
    settlement = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.seller.user.user.username}"

    def save(self, *args, **kwargs):
        self.slug = None
        super().save(*args, **kwargs)
        self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
        if self.originalPrice:
            self._get_item_price()
            super().save(*args, **kwargs)

    def _get_item_price(self):
        self.price = self.originalPrice + (self.gst/100)*self.originalPrice

    def _get_unique_slug(self):
        if self.title:
            slug = slugify(self.title)
            unique_slug = slug
            num = 1
            while Item.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            slug = unique_slug
            return slug
        return uuid.uuid4()


    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })
    
    def get_absolute_url(self):
        return reverse('product', args=[self.slug])


class PackageInformation(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    packageLength = models.FloatField(blank=True, null=True)
    packageWidth = models.FloatField(blank=True, null=True)
    packageHeight = models.FloatField(blank=True, null=True)
    packageWeight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.item.title} package information"

class OrderItem(models.Model):
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Item', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    createdOn = models.DateTimeField(blank=True, null=True)
    affiliatePaid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return round((self.quantity * self.item.price), 2)

    def get_total_discount_item_price(self):
        return round((self.quantity * self.item.discount_price), 2)

    def get_amount_saved(self):
        return round((self.get_total_item_price() - self.get_total_discount_item_price()), 2)

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    '''when the item is ordered'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    item = models.ManyToManyField(
        'OrderItem', related_name="item_list")
    created_on = models.DateField(auto_now_add=True)
    ordered_date = models.DateField(blank=True, null=True)
    billing_date = models.DateField(blank=True, null=True)
    billing_mode = models.CharField(blank=True, null=True, max_length=10)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'users.BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"ORDER_ID_{self.pk}"

    def get_total(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= round(self.coupon.amount, 2)
        return round(total, 2)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class ItemImages(models.Model):
    item = models.ForeignKey(
        'Item', on_delete=models.CASCADE)
    image = ImageField(upload_to="item_images")

    def __str__(self):
        return f"{self.item.title} by {self.item.seller.user.user.username}"

class Comment(models.Model):
    item = models.ForeignKey(
        'Item', on_delete=models.CASCADE, related_name='commented_on')
    rating = models.IntegerField()
    text = models.TextField()
    user = models.ForeignKey('users.UserExtended',
                             on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return f"{self.user} on {self.item}"


@receiver(post_delete, sender=ItemImages)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.image.delete(save=False)

@receiver(post_save, sender= ItemImages)
def delete_old_image(sender, instance, **kwargs):
    if hasattr(instance, '_current_imagen_file'):
        if instance._current_imagen_file != instance.imagen.path:
            instance._current_imagen_file.delete(save=False)