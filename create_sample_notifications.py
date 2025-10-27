"""
Create sample notifications for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from accounts.models import User, Notification
from products.models import Product, Deal
from orders.models import Order

# Get all active users (excluding staff)
users = User.objects.filter(is_active=True, is_staff=False)

if not users.exists():
    print("No regular users found. Please create a user account first.")
    exit()

print(f"Found {users.count()} user(s). Creating sample notifications...")

# Sample notifications data
sample_notifications = [
    {
        'type': 'new_product',
        'title': 'New Product: AMD Ryzen 9 7950X',
        'message': 'Check out our new product: AMD Ryzen 9 7950X at ₱35,999.00!',
        'link': '/products/',
    },
    {
        'type': 'new_deal',
        'title': 'Flash Sale: Up to 50% OFF!',
        'message': 'Limited time offer on selected products. Don\'t miss out!',
        'link': '/deals/',
    },
    {
        'type': 'order_update',
        'title': 'Your order is being processed',
        'message': 'We are preparing your items for shipment.',
        'link': '/account/',
    },
    {
        'type': 'new_product',
        'title': 'New Product: NVIDIA RTX 4090',
        'message': 'The most powerful graphics card is now available at ₱105,999.00!',
        'link': '/products/',
    },
    {
        'type': 'order_shipped',
        'title': 'Your order has been shipped!',
        'message': 'Your package is on the way. Track your order in your account.',
        'link': '/account/',
    },
]

created_count = 0

for user in users:
    for notif_data in sample_notifications:
        notification = Notification.objects.create(
            user=user,
            notification_type=notif_data['type'],
            title=notif_data['title'],
            message=notif_data['message'],
            link=notif_data['link'],
            is_read=False
        )
        created_count += 1
        print(f"✓ Created: {notification.title} for {user.email}")

print(f"\n✅ Successfully created {created_count} notifications!")
print(f"\nNotifications per user:")
for user in users:
    unread = Notification.objects.filter(user=user, is_read=False).count()
    total = Notification.objects.filter(user=user).count()
    print(f"  • {user.email}: {unread} unread / {total} total")
