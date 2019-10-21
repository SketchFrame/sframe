from django.db import models
from users.models import *
from ckeditor.fields import RichTextField
from products.models import *
from sorl.thumbnail import ImageField
from django.dispatch import receiver
from django.db.models.signals import post_delete

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)

class Seller(models.Model):
    user = models.ForeignKey(
        'users.UserExtended', on_delete=models.CASCADE, related_name='seller_from_user', blank=True, null=True)
    registered_date = models.DateField(auto_now_add=True)
    products = models.ManyToManyField(
        'products.Item', blank=True, related_name="sellerItems")
    fname = models.CharField(max_length=40, default="")
    lname = models.CharField(max_length=40, default="")
    gstNumber = models.CharField(max_length=30, default="")
    experience = models.IntegerField(default=0)
    contactNumber = models.CharField(max_length=15, default="")
    speciality = models.CharField(max_length=100, default="")
    gender = models.CharField(choices=GENDER_CHOICES,
                              default="Male", max_length=10)
    profile_img = ImageField(
        upload_to="seller/profile_images/", null=True, blank=True)
    cover_img = ImageField(
        upload_to="seller/cover_images/", null=True, blank=True)
    basic_profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user.username


class SellerAddress(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    zipCode = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    address_profile_completed = models.BooleanField(default=False)

    def _str_(self):
        return self.seller.user.user.username


class SellerExtended(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    rating = models.FloatField(blank=True, null=True)
    totalEarning = models.IntegerField(blank=True, null=True)
    bio = models.TextField(max_length=450)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    Pencil_work = models.BooleanField(default=False)
    Pastel_colours = models.BooleanField(default=False)
    Water_colours = models.BooleanField(default=False)
    Acrylic_colours = models.BooleanField(default=False)
    Fabric_colours = models.BooleanField(default=False)
    Oil_colours = models.BooleanField(default=False)
    Mix_media = models.BooleanField(default=False)
    description_profile_completed = models.BooleanField(default=False)

    def _str_(self):
        return self.seller.user.user.username


class SellerComment(models.Model):
    seller = models.ForeignKey(
        'Seller', on_delete=models.CASCADE, related_name='seller_comments')
    text = RichTextField()
    rating = models.IntegerField(default=0)
    user = models.ForeignKey('users.UserExtended',
                             on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.user} for {self.seller}"


class PortfolioImages(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="seller/portfolio_images/")
    created_on = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=120, null=True, blank=True)

    def _str_(self):
        return f"{self.seller} portfolio image"

    def get_absolute_url(self):
        return reverse('seller-profile')

class Payments(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    accountNumber = models.CharField(max_length=20, null=True, blank=True)
    cif = models.CharField(max_length=20, null=True, blank=True)
    fullName = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"{self.seller} bank details"
@receiver(post_delete, sender=Seller)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.profile_img.delete(save=False)
    instance.cover_img.delete(save=False)
