from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import Item, ItemImages, PackageInformation
from ckeditor.fields import RichTextField


class AddItemCategoryForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'subCategory')


class SellingInformation(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('sku', 'stock', 'listing_status',
                  'price', 'gst', 'dispatch_time',)

        widgets = {
            'sku': forms.TextInput(attrs={'placeholder': "eg. SFRAME100", 'id': 'sku', 'readonly': True}),
            'stock': forms.NumberInput(attrs={'placeholder': "eg. 2", 'id': 'stock'}),
            'listing_status': forms.CheckboxInput(attrs={'class': "custom-control-input", 'id': "publish"}),
            'price': forms.NumberInput(attrs={'placeholder': "eg. 25,000", 'id': 'price'}),
            'gst': forms.TextInput(attrs={'placeholder': "eg. 12%", 'id': 'gst'}),
            'dispatch_time': forms.NumberInput(attrs={'placeholder': "eg. 2 days", 'id': 'dispatchTime'})
        }
        labels = {
            'sku': '',
            'stock': '',
            'price': '',
            'gst': '',
            'dispatch_time': '',
            'listing_status': '',
        }


class productDescription(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'color', 'shortDescription', 'fullDescription',
                  'weight', 'length', 'height', 'hsnCode', 'frameCost', 'addFrame')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "eg. My lovely artwork", 'id': 'title', 'required': True}),
            'color': forms.TextInput(attrs={'placeholder': "eg. Green", 'id': 'color', 'required': True}),
            'shortDescription': forms.TextInput(attrs={'placeholder': "Choose from the wide variety of art, on demand paintings, sketches and a lot more", 'id': "shortDescription", 'required': True}),
            'fullDescription': forms.Textarea(attrs={'placeholder': "Choose from the wide variety of art, on demand paintings, sketches and a lot more. Gifts for your love ones, all at a single hub. Easily accessible and affordable.", 'id': "fullDescription", 'required': True}),
            'weight': forms.NumberInput(attrs={'placeholder': "eg. 750", 'id': 'weight', 'required': True}),
            'length': forms.NumberInput(attrs={'placeholder': "eg. 20", 'id': "length", 'required': True}),
            'height': forms.NumberInput(attrs={'placeholder': "eg. 20", 'id': "height", 'required': True}),
            'hsnCode': forms.TextInput(attrs={'placeholder': "eg. XXXXXXX", 'id': "hsnCode", 'required': True}),
            'frameCost': forms.NumberInput(attrs={'placeholder': "eg. 1000", 'id': "framingCost"}),
            'addFrame': forms.CheckboxInput(attrs={'class': "custom-control-input", 'id': "frame"}),
        }
        labels = {
            'title': '',
            'color': '',
            'shortDescription': '',
            'fullDescription': '',
            'weight': '',
            'length': '',
            'height': '',
            'hsnCode': '',
            'frameCost': '',
            'addFrame': '',
        }


class PackageDetailsForm(forms.ModelForm):
    class Meta:
        model = PackageInformation
        exclude = ('item',)

        widgets = {
            'packageLength': forms.NumberInput(attrs={'placeholder': 'e.g. 40', 'id': 'packageLength', 'required': True}),
            'packageWidth': forms.NumberInput(attrs={'placeholder': 'e.g. 40', 'id': 'packageWidth', 'required': True}),
            'packageHeight': forms.NumberInput(attrs={'placeholder': 'e.g. 40', 'id': 'packageHeight', 'required': True}),
            'packageWeight': forms.NumberInput(attrs={'placeholder': 'e.g. 1000', 'id': 'packageWeight', 'required': True}),
        }

        labels = {
            'packageLength': '',
            'packageWidth': '',
            'packageHeight': '',
            'packageWeight': '',
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
