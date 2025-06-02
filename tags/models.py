from django.db import models

class TagType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, help_text="Optional description of this tag type")
    color = models.CharField(max_length=7, default='#6c757d', help_text="Hex color code for display (e.g., #FF5733)")
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    is_active = models.BooleanField(default=True, help_text="Inactive types won't appear in filters")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Tag Type"
        verbose_name_plural = "Tag Types"
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tag_type = models.ForeignKey(TagType, on_delete=models.CASCADE, related_name='tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['tag_type__sort_order', 'tag_type__name', 'name']
    
    def __str__(self):
        return self.name
    
    def get_color(self):
        """Return the tag type color, or default gray if no tag type"""
        return self.tag_type.color if self.tag_type else '#6c757d'
    
    def get_text_color(self):
        """Return appropriate text color (white or black) based on background color"""
        if not self.tag_type:
            return 'white'
        
        # Convert hex to RGB
        hex_color = self.tag_type.color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Calculate brightness
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        
        # Return black for light colors, white for dark colors
        return 'black' if brightness > 128 else 'white'
