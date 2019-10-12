from django.db import models
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_delete

USER_CHOICE = (
    ('seller', 'seller'),
    ('user', 'user')
)
CATEGORY_CHOICES = (
    ('Pencil work', 'Pencil work'),
    ('Pastel colours', 'Pastel colours'),
    ('Water colours', 'Water colours'),
    ('Acrylic colours', 'Acrylic colours'),
    ('Fabric colours', 'Fabric colours'),
    ('Oil colours', 'Oil colours'),
    ('Mix media', 'Mix Media'),
)

class MainBanner(models.Model):
    order = models.IntegerField()
    image = models.ImageField(upload_to='MainBanner/')

class FAQ(models.Model):
    order = models.IntegerField(unique=True, blank=True, null=True)
    faq_of = models.CharField(choices=USER_CHOICE, max_length=10, default='seller') 
    question = models.CharField(max_length=300)
    answer = RichTextField()

    def __str__(self):
        return f'{self.faq_of} ask\'s, {self.question}'

class AffiliateFAQ(models.Model):
    order = models.IntegerField(unique=True, blank=True, null=True)
    question = models.CharField(max_length=300)
    answer = RichTextField()

    def __str__(self):
        return self.question

class PrivacyPolicy(models.Model):
    order = models.IntegerField()
    content = RichTextField()

class Charges(models.Model):
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=20, unique=True)
    gst = models.FloatField()
    serviceCharge = models.FloatField()

    def __str__(self):
        return f"{self.category} at {self.serviceCharge}%, having GST {self.gst}%"

class ProductAffiliate(models.Model):
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=20, unique=True)
    charge = models.FloatField()

    def __str__(self):
        return f"{self.category} at {self.charge}%"

class SellerAffiliate(models.Model):
    charge = models.FloatField()

    def __str__(self):
        return f"{self.category} at {self.charge}%"

class NewsletterEmails(models.Model):
    email = models.EmailField()
    def __str__(self):
        return f"{self.email}"

class NewsletterMessages(models.Model):
    email = models.ForeignKey(
        'NewsletterEmails', null=True, blank=True, on_delete=models.SET_NULL)
    message = RichTextField()
    # items = models.ForeignKey('products.Item', null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Newsletter created on {self.created_on}"

@receiver(post_delete, sender=MainBanner)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.image.delete(save=False)

