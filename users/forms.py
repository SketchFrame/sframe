from django import forms
from .models import Address, UserExtended

class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'address1',
            'address2',
            'landmark',
            'phone1',
            'phone2',
            'state',
            'country',
            'city',
            'zipCode',
        )
        widgets = {
            'address1': forms.Textarea(attrs={'cols': 1, 'rows': 2, 'placeholder': 'Falt / House No. / Floor / Building'}),
            'address2': forms.Textarea(attrs={'cols': 1, 'rows': 2, 'placeholder': 'Colony / Street / Locality'}),
            'landmark': forms.TextInput(attrs={'cols': 1, 'rows': 2, 'placeholder': 'Colony / Street / Locality'}),
            'phone1': forms.TextInput(attrs={'placeholder': 'Your Mobile Number'}),
            'phone2': forms.TextInput(attrs={'placeholder': 'Alternate Mobile Number'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'placeholder': 'India', 'readonly': True, 'value': 'India'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'zipCode': forms.TextInput(attrs={'placeholder': 'Zip/Pin Code'}),
        }

        labels = {
            'address1': "",
            'address2': "",
            'landmark': "",
            'phone1': "",
            'phone2': "",
            'state': "",
            'country': "",
            'city': "",
            'zipCode': "",
        }

class AddPaymentNumbersForm(forms.ModelForm):
    class Meta:
        model = UserExtended
        fields = (
            'paytm_number',
            'googlePay_number',
        )
        widgets = {
            'paytm_number': forms.TextInput(attrs={'placeholder': 'Paytm number', 'class': 'payment_numbers'}),
            'googlePay_number': forms.TextInput(attrs={'placeholder': 'Google Pay UPI ID', 'class': 'payment_numbers'})
        }
        labels = {
            'paytm_number': '',
            'googlePay_number': '',
        }