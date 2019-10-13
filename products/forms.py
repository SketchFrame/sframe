from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import Item, ItemImages, PackageInformation
from ckeditor.fields import RichTextField

class AddItemCategoryForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'subCategory')

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('seller', 'slug', 'approved', 'price', )
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "eg. My lovely artwork", 'id': 'title'}),
            'sku': forms.TextInput(attrs={'placeholder': "eg. SFRAME100", 'id': 'sku'}),
            'stock': forms.NumberInput(attrs={'placeholder': "eg. 2", 'id': 'stock'}),
            'originalPrice': forms.NumberInput(attrs={'placeholder': "eg. 25,000", 'id': 'price'}),
            'gst': forms.TextInput(attrs={'placeholder': "your GST number", 'id': 'gst'}),
            'makingTime': forms.NumberInput(attrs={'placeholder': "eg. 2 days", 'id': 'dispatchTime'}),
            'published': forms.CheckboxInput(attrs={'class': "custom-control-input", 'id': "publish"}),
            'colour': forms.TextInput(attrs={'placeholder': "eg. Green", 'id': 'color'}),
            'shortDescription': forms.TextInput(attrs={'placeholder': "Choose from the wide variety of art, on demand paintings, sketches and a lot more", 'id': "shortDescription"}),
            'description': forms.Textarea(attrs={'placeholder': "Choose from the wide variety of art, on demand paintings, sketches and a lot more. Gifts for your love ones, all at a single hub. Easily accessible and affordable.", 'id': "fullDescription"}),
            'weight': forms.NumberInput(attrs={'placeholder': "eg. 750", 'id':'weight'}),
            'length': forms.NumberInput(attrs={'placeholder': "eg. 20", 'id': "length"}),
            'height': forms.NumberInput(attrs={'placeholder': "eg. 20", 'id': "height"}),
            'hsn': forms.TextInput(attrs={'placeholder': "eg. XXXXXXX", 'id': "hsnCode"}),
            'frameCost': forms.NumberInput(attrs={'placeholder': "eg. 1000", 'id':"framingCost"}),
            'addFrame': forms.CheckboxInput(attrs={'class': "custom-control-input", 'id': "frame"}),
        }
        labels = {
            'title': '',
            'sku': '',
            'stock': '',
            'originalPrice': '',
            'gst': '',
            'makingTime': '',
            'published': '',
            'colour': '',
            'shortDescription': '',
            'description': '',
            'weight': '',
            'length': '',
            'height': '',
            'hsn': '',
            'frameCost': '',
            'addFrame': '',
        }

class PackageDetailsForm(forms.ModelForm):
    class Meta:
        model = PackageInformation
        exclude = ('item',)

        widgets = {
            'packageLength': forms.NumberInput(attrs={'placeholder': 'e.g. 40', 'id': 'packageLength'}),
            'packageWidth': forms.NumberInput(attrs={'placeholder': 'e.g. 40', 'id': 'packageWidth'}),
            'packageHeight': forms.NumberInput(attrs={'placeholder': 'e.g. 40', 'id': 'packageHeight'}),
            'packageWeight': forms.NumberInput(attrs={'placeholder': 'e.g. 1000', 'id': 'packageWeight'}),
        }

class EditProduct(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('seller', 'slug', 'approved', 'price', )
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "eg. My lovely artwork", 'id': 'title'}),
            'sku': forms.TextInput(attrs={'placeholder': "eg. SFRAME100", 'id': 'sku'}),
            'stock': forms.NumberInput(attrs={'placeholder': "eg. 2", 'id': 'stock'}),
            'originalPrice': forms.NumberInput(attrs={'placeholder': "eg. 25,000", 'id': 'price'}),
            'gst': forms.TextInput(attrs={'placeholder': "your GST number", 'id': 'gst'}),
            'makingTime': forms.NumberInput(attrs={'placeholder': "eg. 2 days", 'id': 'dispatchTime'}),
            'published': forms.CheckboxInput(attrs={'class': "custom-control-input", 'id': "publish"}),
            'colour': forms.TextInput(attrs={'placeholder': "eg. Green", 'id': 'color'}),
            'shortDescription': forms.TextInput(attrs={'placeholder': "Choose from the wide variety of art, on demand paintings, sketches and a lot more", 'id': "shortDescription"}),
            'description': forms.Textarea(attrs={'placeholder': "Choose from the wide variety of art, on demand paintings, sketches and a lot more. Gifts for your love ones, all at a single hub. Easily accessible and affordable.", 'id': "fullDescription"}),
            'weight': forms.NumberInput(attrs={'placeholder': "eg. 750", 'id':'weight'}),
            'length': forms.NumberInput(attrs={'placeholder': "eg. 20", 'id': "length"}),
            'height': forms.NumberInput(attrs={'placeholder': "eg. 20", 'id': "height"}),
            'hsn': forms.TextInput(attrs={'placeholder': "eg. XXXXXXX", 'id': "hsnCode"}),
            'frameCost': forms.NumberInput(attrs={'placeholder': "eg. 1000", 'id':"framingCost"}),
            'addFrame': forms.CheckboxInput(attrs={'class': "custom-control-input", 'id': "frame"}),
        }
        labels = {
            'title': '',
            'sku': '',
            'stock': '',
            'originalPrice': '',
            'gst': '',
            'makingTime': '',
            'published': '',
            'colour': '',
            'shortDescription': '',
            'description': '',
            'weight': '',
            'length': '',
            'height': '',
            'hsn': '',
            'frameCost': '',
            'addFrame': '',
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