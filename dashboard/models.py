from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class SlideshowImage(models.Model):
    """Model for homepage slideshow images"""
    SLIDE_TYPE_CHOICES = [
        ('main', 'Main Slideshow'),
        ('banner', 'Static Banner'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='slideshow/')
    slide_type = models.CharField(max_length=10, choices=SLIDE_TYPE_CHOICES, default='main')
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    link = models.CharField(max_length=500, blank=True, help_text="Optional link URL")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Slideshow Image'
        verbose_name_plural = 'Slideshow Images'
    
    def __str__(self):
        return f"{self.title} ({self.get_slide_type_display()})"
