"""
Fix notification links to redirect to products list page
Run this script to update notification links
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from accounts.models import Notification

# Find all new_product notifications
notifications = Notification.objects.filter(notification_type='new_product')

count = notifications.count()
print(f"Found {count} new product notifications")

if count > 0:
    # Update all to point to products list page
    updated = notifications.update(link='/products/')
    print(f"✅ Updated {updated} notification links!")
    print("All new product notifications now redirect to: /products/")
else:
    print("✅ No new product notifications found!")
