from django import forms
from .models import Tag, TagType

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'tag_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tag_type': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active tag types
        self.fields['tag_type'].queryset = TagType.objects.filter(is_active=True)

class TagTypeForm(forms.ModelForm):
    class Meta:
        model = TagType
        fields = ['name', 'description', 'color', 'sort_order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
