from django import forms
from products.models import Comment

STATE_CHOICES = (
    ('DEF', '(select state)'),
    ('Andra Pradesh', 'Andra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madya Pradesh', 'Madya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telagana', 'Telagana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control no-bg',
         'placeholder' :"Name",
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control no-bg',
         'placeholder' :"Email",
         'type': 'email'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "rows":6,
        'placeholder': 'Your message',
        'class': 'form-control no-bg'
    }))

class ContactForm2(forms.Form):
    messageBox = forms.CharField(widget=forms.Textarea(attrs={
        "rows":2,
        'placeholder': 'Leave us a message',
        'class': 'form-control',
        'style': 'border:none'
    }))

class CheckoutForm(forms.Form):
    fullname = forms.CharField()

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

class EditProductComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'rating',
            'text',
        ]