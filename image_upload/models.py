from django.db import models
from tags.models import Tag

class Image(models.Model):
    # File field for STL files
    image = models.ImageField(upload_to='uploaded_images/')
    
    # Basic information
    name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    range = models.CharField(max_length=255, blank=True, null=True)
    folder_location = models.CharField(max_length=500, blank=True, null=True)
    
    # Metadata
    upload_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    # Many-to-many relationship with tags
    tags = models.ManyToManyField(Tag, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.name
