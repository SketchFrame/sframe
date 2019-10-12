from django import forms
from .models import project, Bids


class PostProjectForm(forms.ModelForm):

    class Meta:
        model = project
        fields = [
            'title',
            'category',
            'description',
            'budget',
            'sampleImage'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Build a sketch on Mahatma Gandhi', 'class': 'project-title', 'id': 'project-title'}),
            'description': forms.Textarea(attrs={'placeholder': 'e.g. Mahatma Gandhi was a non-violent man and he was one of the most greatest freedom fighter for india, in the sketch make sure to portray this quality of Mahatma Gandhi', 'class': 'project-description', 'id': 'project-description'}),
            'sampleImage': forms.ClearableFileInput(attrs={'class': "upload-file", })
        }
        labels = {
            'image': '',
        }


class BidProjectForm(forms.ModelForm):

    class Meta:
        model = Bids
        fields = [
            'proposal',
            'amount',
            'delivery_in',
        ]


class BidUpdateForm(forms.ModelForm):

    class Meta:
        model = Bids
        fields = [
            'proposal',
            'amount',
            'delivery_in',
        ]
