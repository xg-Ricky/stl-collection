from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class ColorPickerWidget(forms.TextInput):
    """A custom widget that provides a modern HTML5 color picker with text input fallback"""
    
    input_type = 'color'
    
    def __init__(self, attrs=None):
        default_attrs = {
            'style': 'width: 60px; height: 40px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        """Ensure the value is in the correct format for the color input"""
        if value and not value.startswith('#'):
            value = f'#{value}'
        return value or '#6c757d'
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render both color picker and text input for better UX"""
        if attrs is None:
            attrs = {}
        
        # Format the value
        formatted_value = self.format_value(value)
        
        # Create the color picker
        color_attrs = self.build_attrs(attrs, extra_attrs={
            'type': 'color',
            'value': formatted_value,
            'id': f'id_{name}_color'
        })
        
        # Create the text input for manual entry
        text_attrs = {
            'type': 'text',
            'value': formatted_value,
            'id': f'id_{name}',
            'name': name,
            'maxlength': '7',
            'style': 'width: 100px; margin-left: 8px; font-family: monospace;',
            'placeholder': '#6c757d'
        }
          # JavaScript to sync the two inputs
        script = f'''
<script>
document.addEventListener('DOMContentLoaded', function() {{
    var colorInput = document.getElementById('id_{name}_color');
    var textInput = document.getElementById('id_{name}');
    
    if (colorInput && textInput) {{
        colorInput.addEventListener('input', function() {{
            textInput.value = this.value;
        }});
        
        textInput.addEventListener('input', function() {{
            var value = this.value;
            if (value.match(/^#[0-9A-Fa-f]{{6}}$/)) {{
                colorInput.value = value;
            }}
        }});
    }}
}});
</script>
'''
        
        # Create the HTML structure
        html = f'''
<div style="display: flex; align-items: center; gap: 8px;">
    <input{flatatt(color_attrs)} />
    <input{flatatt(text_attrs)} />
    <small style="color: #666;">Click color box or enter hex code</small>
</div>
{script}
'''
        
        return mark_safe(html)
