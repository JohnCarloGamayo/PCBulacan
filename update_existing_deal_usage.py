"""
Script to update deal usage count for existing processed orders
Run this once to count deals from orders that were already processed
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from orders.models import Order
from products.models import Deal
from django.utils import timezone
from django.db.models import F

def update_deal_usage():
    """Update deal usage count for existing processed orders"""
    
    # Get all processed orders that haven't been counted yet
    processed_orders = Order.objects.filter(
        status__in=['processing', 'shipped', 'delivered', 'received'],
        deal_usage_counted=False
    ).order_by('created_at')
    
    print(f"Found {processed_orders.count()} processed orders without deal usage counted")
    
    deals_updated = {}
    
    for order in processed_orders:
        print(f"\nProcessing order: {order.order_number} (Status: {order.status})")
        
        # Track which deals have been used in this order
        deals_used = set()
        
        for item in order.items.all():
            product = item.product
            
            # Check if product had an active deal at the time of order
            # We check deals that were active during order creation
            active_deals = product.deals.filter(
                status='active',
                start_date__lte=order.created_at,
                end_date__gte=order.created_at
            )
            
            for deal in active_deals:
                if deal.id not in deals_used:
                    deals_used.add(deal.id)
                    print(f"  - Product {product.name} had deal: {deal.title}")
        
        # Increment usage count for all deals used in this order
        if deals_used:
            for deal_id in deals_used:
                deal = Deal.objects.get(id=deal_id)
                old_uses = deal.current_uses
                Deal.objects.filter(id=deal_id).update(current_uses=F('current_uses') + 1)
                deal.refresh_from_db()
                
                if deal_id not in deals_updated:
                    deals_updated[deal_id] = {'title': deal.title, 'count': 0}
                deals_updated[deal_id]['count'] += 1
                
                print(f"  ✓ Updated deal '{deal.title}' usage count ({old_uses} → {deal.current_uses})")
            
            order.deal_usage_counted = True
            order.save()
            print(f"  ✓ Marked order as counted")
        else:
            print(f"  - No deals found for this order")
            order.deal_usage_counted = True
            order.save()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total orders processed: {processed_orders.count()}")
    print(f"Total deals updated: {len(deals_updated)}")
    
    if deals_updated:
        print("\nDeal usage updates:")
        for deal_id, info in deals_updated.items():
            print(f"  - {info['title']}: +{info['count']} uses")
    
    print("\n✓ Update completed successfully!")

if __name__ == '__main__':
    update_deal_usage()
