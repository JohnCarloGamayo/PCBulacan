# Simple script to create sample deals
from django.utils import timezone
from products.models import Deal, Product
from accounts.models import User
from datetime import timedelta

# Get admin user
admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    print("No admin user found!")
else:
    print(f"Using admin: {admin_user.email}")
    
    # Get products
    products = list(Product.objects.filter(is_active=True)[:10])
    if not products:
        print("No products found!")
    else:
        print(f"Found {len(products)} products")
        
        now = timezone.now()
        
        # Create deals
        deals = [
            {
                'title': 'Black Friday Mega Sale',
                'description': 'Massive discounts on selected PC components!',
                'deal_type': 'percentage',
                'discount_percentage': 25,
                'badge_text': 'HOT DEAL',
                'is_featured': True,
                'status': 'active',
                'start_date': now,
                'end_date': now + timedelta(days=7),
                'created_by': admin_user
            },
            {
                'title': 'Weekend Flash Sale',
                'description': 'Get PHP 500 off on all processors!',
                'deal_type': 'fixed',
                'discount_amount': 500,
                'badge_text': 'FLASH SALE',
                'is_featured': True,
                'status': 'active',
                'start_date': now,
                'end_date': now + timedelta(days=3),
                'created_by': admin_user
            },
        ]
        
        for deal_data in deals:
            if not Deal.objects.filter(title=deal_data['title']).exists():
                deal = Deal.objects.create(**deal_data)
                deal.products.set(products[:5])
                deal.apply_to_products()
                print(f"Created: {deal.title}")
            else:
                print(f"Exists: {deal_data['title']}")
        
        print(f"\nTotal deals: {Deal.objects.filter(status='active').count()}")
        print(f"Products on sale: {Product.objects.filter(on_sale=True).count()}")
