from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAddress, Notification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def profile_pic_thumb(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />'
        return ''
    profile_pic_thumb.short_description = 'Profile Picture'
    profile_pic_thumb.allow_tags = True

    list_display = ('profile_pic_thumb', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('user__email', 'address_line1', 'city', 'state')
    ordering = ('-created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as unread"
