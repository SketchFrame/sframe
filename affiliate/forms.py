from django import forms
from affiliate.models import ProductAffiliate

class AddArtworkAffiliate(forms.ModelForm):
    class Meta:
        model = ProductAffiliate
        fields = [
            'item',
        ]
        widgets = {
            'item': forms.TextInput(attrs={'required': True,})
        }
        labels = {
            'item': 'Artwork',
        }
