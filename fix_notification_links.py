"""
Fix notification links from /products/ to /product/
Run this script to fix existing notifications with wrong URLs
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from accounts.models import Notification

# Find all notifications with wrong product links
notifications = Notification.objects.filter(link__startswith='/products/')

count = notifications.count()
print(f"Found {count} notifications with wrong links")

if count > 0:
    # Update the links
    for notif in notifications:
        # Replace /products/ with /product/
        notif.link = notif.link.replace('/products/', '/product/', 1)
        notif.save()
    
    print(f"✅ Fixed {count} notification links!")
    print("Changed from: /products/<slug>/")
    print("Changed to:   /product/<slug>/")
else:
    print("✅ No notifications need fixing!")
