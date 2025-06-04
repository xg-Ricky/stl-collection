from django import forms
from .models import Image
from tags.models import Tag

class ImageUploadForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'data-live-search': 'true',
            'multiple': True
        }),
        required=False
    )
    
    class Meta:
        model = Image
        fields = ['image', 'name', 'publisher', 'range', 'folder_location', 'notes', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'range': forms.TextInput(attrs={'class': 'form-control'}),
            'folder_location': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class ImageEditForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'data-live-search': 'true',
            'multiple': True
        }),
        required=False
    )
    
    class Meta:
        model = Image
        fields = ['name', 'publisher', 'range', 'folder_location', 'notes', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'range': forms.TextInput(attrs={'class': 'form-control'}),
            'folder_location': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }
