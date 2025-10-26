from django.contrib import admin
from .models import SlideshowImage

# Register your models here.

@admin.register(SlideshowImage)
class SlideshowImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slide_type', 'order', 'is_active', 'created_at']
    list_filter = ['slide_type', 'is_active']
    search_fields = ['title', 'link']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_at']
