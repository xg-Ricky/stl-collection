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
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Fantasy, Sci-Fi, Terrain'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Optional description of this tag type...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'style': 'height: 50px;'
            }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].help_text = "A descriptive name for this tag category"
        self.fields['description'].help_text = "Optional description explaining what tags of this type represent"
        self.fields['color'].help_text = "Color used to display tags of this type (click to open color picker)"
        self.fields['sort_order'].help_text = "Lower numbers appear first in lists (0 = first)"
        self.fields['is_active'].help_text = "Inactive types won't appear in tag creation forms"
