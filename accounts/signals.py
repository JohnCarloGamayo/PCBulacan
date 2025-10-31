"""
Signal handlers for creating notifications
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from products.models import Product, Deal
from orders.models import Order
from .models import Notification, User


# Track old status before save
@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    """Track the old status before saving"""
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            instance._old_status = old_order.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Product)
def create_new_product_notification(sender, instance, created, **kwargs):
    """Create notification when a new product is added"""
    if created and instance.is_active:
        # Create notification for all active users
        users = User.objects.filter(is_active=True, is_staff=False)
        
        notifications = []
        # Format price safely
        try:
            price_display = f"₱{float(instance.price):,.2f}"
        except (ValueError, TypeError):
            price_display = f"₱{instance.price}"
        
        for user in users:
            notifications.append(
                Notification(
                    user=user,
                    notification_type='new_product',
                    title=f'New Product: {instance.name}',
                    message=f'Check out our new product: {instance.name} at {price_display}!',
                    link='/products/',
                    product_id=instance.id
                )
            )
        
        # Bulk create notifications for efficiency
        if notifications:
            Notification.objects.bulk_create(notifications)
            print(f"✅ Created {len(notifications)} notifications for new product: {instance.name}")


@receiver(post_save, sender=Deal)
def create_new_deal_notification(sender, instance, created, **kwargs):
    """Create notification when a new deal is created or activated"""
    if (created or instance.status == 'active') and instance.is_active():
        # Create notification for all active users
        users = User.objects.filter(is_active=True, is_staff=False)
        
        notifications = []
        for user in users:
            notifications.append(
                Notification(
                    user=user,
                    notification_type='new_deal',
                    title=f'New Deal: {instance.title}',
                    message=f'{instance.description} - {instance.get_discount_display()}',
                    link='/deals/',
                    deal_id=instance.id
                )
            )
        
        # Bulk create notifications for efficiency
        if notifications:
            Notification.objects.bulk_create(notifications)
            print(f"✅ Created {len(notifications)} notifications for new deal: {instance.title}")


@receiver(post_save, sender=Order)
def create_order_update_notification(sender, instance, created, **kwargs):
    """Create notification when order status changes"""
    if created:
        # New order created
        Notification.objects.create(
            user=instance.user,
            notification_type='order_update',
            title=f'Order {instance.order_number} Received',
            message=f'We received your order! Total: ₱{instance.total:,.2f}',
            link='/accounts/account/',
            order_id=instance.id
        )
        print(f"✅ Created notification for new order: {instance.order_number}")
    else:
        # Check if status was updated
        if hasattr(instance, '_old_status') and instance._old_status != instance.status:
            # Status was updated
            status_messages = {
                'pending': 'Your order is pending confirmation.',
                'processing': 'Your order is being processed!',
                'shipped': 'Your order has been shipped! 📦',
                'delivered': 'Your order has been delivered! 🎉',
                'received': 'Thank you for confirming receipt!',
                'cancelled': 'Your order has been cancelled.'
            }
            
            notification_type = 'order_shipped' if instance.status == 'shipped' else \
                               'order_delivered' if instance.status == 'delivered' else \
                               'order_update'
            
            Notification.objects.create(
                user=instance.user,
                notification_type=notification_type,
                title=f'Order {instance.order_number} Update',
                message=status_messages.get(instance.status, f'Your order status is now {instance.status}.'),
                link='/accounts/account/',
                order_id=instance.id
            )
            print(f"✅ Created notification for order status change: {instance.order_number} ({instance._old_status} → {instance.status})")
            
            # Notify admin when order is received
            if instance.status == 'received':
                admin_users = User.objects.filter(is_staff=True, is_active=True)
                for admin in admin_users:
                    Notification.objects.create(
                        user=admin,
                        notification_type='order_update',
                        title=f'Order Received: {instance.order_number}',
                        message=f'Customer has confirmed receipt of order {instance.order_number}',
                        link=f'/dashboard/orders/{instance.order_number}/details/',
                        order_id=instance.id
                    )
                print(f"✅ Notified admins about received order: {instance.order_number}")


# Admin Notifications

@receiver(post_save, sender=User)
def notify_admin_new_user(sender, instance, created, **kwargs):
    """Notify admin when a new user registers"""
    if created and not instance.is_staff:
        admin_users = User.objects.filter(is_staff=True, is_active=True)
        
        notifications = []
        for admin in admin_users:
            notifications.append(
                Notification(
                    user=admin,
                    notification_type='new_user',
                    title='New User Registration',
                    message=f'{instance.get_full_name() or instance.email} has registered an account',
                    link='/dashboard/users/'
                )
            )
        
        if notifications:
            Notification.objects.bulk_create(notifications)
            print(f"✅ Notified {len(notifications)} admins about new user: {instance.email}")


@receiver(post_save, sender=Product)
def notify_admin_low_stock(sender, instance, **kwargs):
    """Notify admin when product stock is low (10 or less)"""
    if instance.stock <= 10 and instance.stock > 0 and instance.is_active:
        # Check if we already sent a low stock notification recently (within 24 hours)
        recent_notification = Notification.objects.filter(
            notification_type='system',
            product_id=instance.id,
            title__contains='Low Stock Alert',
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).exists()
        
        if not recent_notification:
            admin_users = User.objects.filter(is_staff=True, is_active=True)
            
            notifications = []
            for admin in admin_users:
                notifications.append(
                    Notification(
                        user=admin,
                        notification_type='system',
                        title=f'Low Stock Alert: {instance.name}',
                        message=f'Only {instance.stock} units left in stock!',
                        link=f'/dashboard/products/',
                        product_id=instance.id
                    )
                )
            
            if notifications:
                Notification.objects.bulk_create(notifications)
                print(f"⚠️ Notified {len(notifications)} admins about low stock: {instance.name} ({instance.stock} left)")


@receiver(post_save, sender=Order)
def notify_admin_new_order(sender, instance, created, **kwargs):
    """Notify admins when a new order is placed"""
    if created and instance.status == 'pending':
        admin_users = User.objects.filter(is_staff=True, is_active=True)
        
        notifications = []
        for admin in admin_users:
            notifications.append(
                Notification(
                    user=admin,
                    notification_type='order_update',
                    title=f'New Order #{instance.order_number}',
                    message=f'New order from {instance.user.get_full_name() or instance.user.email} - ₱{instance.total:,.2f}',
                    link='/dashboard/orders/',
                    order_id=instance.id
                )
            )
        
        if notifications:
            Notification.objects.bulk_create(notifications)
            print(f"✅ Notified {len(notifications)} admins about new order: {instance.order_number}")


@receiver(post_save, sender=Order)
def notify_admin_order_received(sender, instance, created, **kwargs):
    """Notify admins when customer marks order as received"""
    if not created:
        # Check if status changed to 'received'
        if hasattr(instance, '_old_status') and instance._old_status != 'received' and instance.status == 'received':
            admin_users = User.objects.filter(is_staff=True, is_active=True)
            
            notifications = []
            for admin in admin_users:
                notifications.append(
                    Notification(
                        user=admin,
                        notification_type='order_delivered',
                        title=f'Order Received: #{instance.order_number}',
                        message=f'{instance.user.get_full_name() or instance.user.email} confirmed receipt of order',
                        link='/dashboard/orders/',
                        order_id=instance.id
                    )
                )
            
            if notifications:
                Notification.objects.bulk_create(notifications)
                print(f"✅ Notified {len(notifications)} admins: Order {instance.order_number} received by customer")
