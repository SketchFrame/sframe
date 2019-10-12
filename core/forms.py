from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        "class": "form-control",
        'placeholder': 'Name'
        }), label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        'placeholder': 'Email'
        }), label="")
    contact_no = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        "class": "form-control",
        'placeholder': 'Your mobile number'
        }), label="")
    message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        "class": "form-control",
        'placeholder': 'Your message',
        'rows': "5"
        }), label="")

    class Meta:
        fields = [
            'name',
            'email',
            'contact_no',
            'message'
        ]
