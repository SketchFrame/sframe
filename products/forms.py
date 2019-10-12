from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import Item, ItemImages
from ckeditor.fields import RichTextField


class AddItemForm(forms.ModelForm):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    discount_price = models.FloatField()
    description = RichTextField()

    class Meta:
        model = Item
        fields = [
            'title',
            'originalPrice',
            'category',
            'subCategory',
            'originalDiscount_price',
            'description',
            'shortDescription',
            'makingTime',
            'stock',
            'published',
            'height',
            'width',
            'weight',
        ]
        widgets = {
            'shortDescription': forms.Textarea(attrs={'col': '1', 'rows': '2'})
        }
        labels = {
            'published': 'Publish',
            'height': 'Height (inches)',
            'width': 'Width (inches)',
            'weight': 'Weight (grams)', 
            'subCategory': 'Sub Category',
            'originalPrice': 'Price',
            'originalDiscount_price': 'Discount Price'
        }

class EditProduct(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title',
            'originalPrice',
            'originalDiscount_price',
            'shortDescription',
            'description',
            'category',
            'makingTime',
            'published',
            'height',
            'width',
            'weight',
            'stock',
            'subCategory'
        ]
        labels = {
            'published': 'Publish',
            'height': 'Height (inches)',
            'width': 'Width (inches)',
            'weight': 'Weight (grams)', 
            'subCategory': 'Sub Category',
            'originalPrice': 'Price',
            'originalDiscount_price': 'Discount Price'
        }


class AddItemImagesForm(forms.ModelForm):
    image = models.ImageField()

    class Meta:
        model = ItemImages
        fields = ('image', )

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': "upload-file", })
        }
        labels = {
            'image': '',
        }


class EditProductImagesForm(forms.ModelForm):
    image = models.ImageField()

    class Meta:
        model = ItemImages
        fields = ('image',)
