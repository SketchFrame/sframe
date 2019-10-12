from django import forms
from django.shortcuts import get_object_or_404
from seller.models import (
    Seller,
    SellerAddress,
    SellerExtended,
    SellerComment,
    PortfolioImages
)


class SellerAddressForm(forms.ModelForm):

    class Meta:
        model = SellerAddress
        fields = [
            'zipCode',
            'city',
            'state',
            'country',
        ]
        widgets = {
            'zipCode': forms.TextInput(attrs={'class': 'zip-code', 'id': 'zip-code', 'maxlength': 6, 'required': True, 'placeholder': 'e.g. 263139'}),
            'city': forms.TextInput(attrs={'class': 'city', 'id': 'city', 'required': True, 'placeholder': 'e.g. Haldwani'}),
            'state': forms.TextInput(attrs={'class': 'state', 'id': 'state', 'required': True, 'placeholder': 'e.g. Uttrakhand'}),
            'country': forms.TextInput(attrs={'class': 'country', 'id': 'country', 'required': True, 'placeholder': 'e.g. India'}),
        }
        labels = {
            'zipCode': 'Zip Code',
            'city': 'City',
            'state': 'State',
            'country': 'Country'
        }


class SellerDetialsForm(forms.ModelForm):

    class Meta:
        model = Seller
        fields = [
            'fname',
            'lname',
            'gstNumber',
            'experience',
            'specialty',
            'gender',
        ]

        widgets = {
            'fname': forms.TextInput(attrs={'class': 'fname', 'id': 'fname', 'required': True, 'placeholder': 'e.g. Debasis'}),
            'lname':  forms.TextInput(attrs={'class': 'lname', 'id': 'lname', 'required': True, 'placeholder': 'e.g. Ghosh'}),
            'gstNumber': forms.TextInput(attrs={'placeholder': 'GST Number'}),
            'experience': forms.NumberInput(attrs={'placeholder': "in years"}),
            'specialty': forms.TextInput(attrs={'placeholder': "e.g. Landscape or Art Acrylic"}),
        }
        labels = {
            'fname': 'First Name',
            'lname': 'Last Name',
            'gstNumber': "GST Registration Number(For Indian Artists)",
            'experience': "Since how many years have you been selling Art ?",
            'specialty': "Your special art form ?",
            'gender': "Gender",
        }

class SellerImages(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            'profile_img',
            'cover_img',
        ]

        widgets = {
            'profile_img': forms.ClearableFileInput(attrs={'class': 'profile-img'}),
            'cover_img': forms.ClearableFileInput(attrs={'class': 'cover-img'}),
        }
        labels = {
            'profile_img': '',
            'cover_img': '',
        }

class SellerExtendedForm(forms.ModelForm):
    class Meta:
        model = SellerExtended
        fields = [
            'bio',
            'facebook',
            'instagram',
            'youtube',
            'twitter',
            'linkedin',
            'Pencil_work',
            'Pastel_colours',
            'Water_colours',
            'Acrylic_colours',
            'Fabric_colours',
            'Oil_colours',
            'Mix_media',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 1, 'rows': 4, 'placeholder': 'I am a seller from north india and I am blah blah blah...'}),
            'facebook': forms.TextInput(attrs={'placeholder': 'https://www.facebook.com/t-series'}),
            'instagram': forms.TextInput(attrs={'placeholder': 'https://www.instagram.com/t-series'}),
            'youtube': forms.TextInput(attrs={'placeholder': 'https://www.youtube.com/t-series'}),
            'twitter': forms.TextInput(attrs={'placeholder': 'https://www.twitter.com/t-series'}),
            'linkedin': forms.TextInput(attrs={'placeholder': 'https://www.linkedin.com/t-series'}),
            'Pencil_work': forms.CheckboxInput(attrs={'id': 'pencil-work'}),
            'Pastel_colours': forms.CheckboxInput(attrs={'id': 'pastel-colors'}),
            'Water_colours': forms.CheckboxInput(attrs={'id': 'water-colors'}),
            'Acrylic_colours': forms.CheckboxInput(attrs={'id': 'acrylic-colors'}),
            'Fabric_colours': forms.CheckboxInput(attrs={'id': 'fabrix-colors'}),
            'Oil_colours': forms.CheckboxInput(attrs={'id': 'oil-colors'}),
            'Mix_media': forms.CheckboxInput(attrs={'id': 'mix-media'}),
        }


class EditCommentsForm(forms.ModelForm):

    class Meta:
        model = SellerComment
        fields = [
            'text',
        ]


class PortfolioImagesForm(forms.ModelForm):

    class Meta:
        model = PortfolioImages
        fields = [
            'image',
            'caption'
        ]


class EditBioForm(forms.ModelForm):

    class Meta:
        model = SellerExtended
        fields = [
            'bio'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'col': 1, 'rows': 4})
        }


class EditSkillsForm(forms.ModelForm):

    class Meta:
        model = SellerExtended
        fields = [
            'Pencil_work',
            'Pastel_colours',
            'Water_colours',
            'Acrylic_colours',
            'Fabric_colours',
            'Oil_colours',
            'Mix_media',
        ]

        widgets = {
            'Pencil_work': forms.CheckboxInput(attrs={'id': 'pencil-work'}),
            'Pastel_colours': forms.CheckboxInput(attrs={'id': 'pastel-colors'}),
            'Water_colours': forms.CheckboxInput(attrs={'id': 'water-colors'}),
            'Acrylic_colours': forms.CheckboxInput(attrs={'id': 'acrylic-colors'}),
            'Fabric_colours': forms.CheckboxInput(attrs={'id': 'fabrix-colors'}),
            'Oil_colours': forms.CheckboxInput(attrs={'id': 'oil-colors'}),
            'Mix_media': forms.CheckboxInput(attrs={'id': 'mix-media'}),
        }

class EditSocialInfoForm(forms.ModelForm):

    class Meta:
        model = SellerExtended
        fields = [
            'facebook',
            'instagram',
            'youtube',
            'twitter',
            'linkedin',
        ]
