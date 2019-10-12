from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.utils.text import slugify
from users.models import *
from notifications.models import Notifications


CATEGORY_CHOICES = (
    ('Pencil work', 'Pencil work'),
    ('Pastel colours', 'Pastel colours'),
    ('Water colours', 'Water colours'),
    ('Acrylic colours', 'Acrylic colours'),
    ('Fabric colours', 'Fabric colours'),
    ('Oil colours', 'Oil colours'),
    ('Mix media', 'Mix media'),
)

BUDGET_CHOICES = (
    ('Less then 3000', 'Less then 3000'),
    ('4000 - 7000', '4000 - 7000'),
    ('8000 - 13000', '8000 - 13000'),
    ('14000 - 18000', '14000 - 18000'),
    ('19000 - 24000', '19000 - 24000'),
    ('More than 24000', 'More than 24000'),
)

class project(models.Model):
    user = models.ForeignKey('users.UserExtended',
                             on_delete=models.CASCADE, related_name='project_by', blank=True, null=True)
    title = models.CharField(
        max_length=200, verbose_name="Choose a name for your project")
    description = models.TextField(
        verbose_name="Describe a little bit about your project")
    slug = models.SlugField(unique=True, blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=25,
                                verbose_name="Tell us the category of your project")
    is_active = models.BooleanField(default=True)
    is_assigned = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    assignedTo = models.ForeignKey(
        'users.UserExtended', on_delete=models.CASCADE, blank=True, null=True)
    assignedOn = models.DateTimeField(null=True, blank=True)
    completedOn = models.DateTimeField(null=True,blank=True)
    budget = models.CharField(choices=BUDGET_CHOICES, max_length=35,
                              verbose_name="Tell us the budget for your project")
    sampleImage = models.ImageField(blank=True, null=True, upload_to="project_images")

    def __str__(self):
        return f"{self.title} by {self.user}"

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while project.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        slug = unique_slug
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Bids(models.Model):
    project = models.ForeignKey(
        'project', on_delete=models.CASCADE, related_name='bid_on')
    user = models.ForeignKey('seller.Seller',
                             on_delete=models.CASCADE, related_name='bid_by', blank=True, null=True)
    bided_on = models.DateTimeField(auto_now_add=True)
    delivery_in = models.IntegerField()
    amount = models.FloatField()
    proposal = models.TextField(max_length=300)

    def get_absolute_url(self):
        return reverse('view-projects')

    def __str__(self):
        return f"{self.user} on {self.project}"


@receiver(post_save, sender=Bids)
def generateNotification(instance, created, **kwargs):
    if created:
        bidCreated = Bids.objects.get(pk=instance.id)
        Notifications.objects.create(
            title="You have a new bid on your Project",
            created_on=timezone.now(),
            bid=instance,
            user=bidCreated.project.user,
            description=f"You are seeing This message because you have a bid on your project with name {bidCreated.project.title} posted on < kbd > {bidCreated.project.posted_date} < /kbd >",
            category="BidAdded"
        )
