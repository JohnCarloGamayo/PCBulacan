"""
Script to create sample deals for testing
Run: python manage.py shell < create_sample_deals.py
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from django.utils import timezone
from products.models import Deal, Product
from accounts.models import User

# Get or create admin user
admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    print("❌ No admin user found! Please create an admin first.")
    exit()

print(f"✓ Using admin user: {admin_user.email}")

# Get some products
products = Product.objects.filter(is_active=True)[:10]
if not products:
    print("❌ No active products found! Please add products first.")
    exit()

print(f"✓ Found {products.count()} products")

# Create sample deals
deals_data = [
    {
        'title': 'Black Friday Mega Sale',
        'description': 'Massive discounts on selected PC components! Limited time only.',
        'deal_type': 'percentage',
        'discount_percentage': 25,
        'badge_text': 'HOT DEAL',
        'is_featured': True,
        'status': 'active',
    },
    {
        'title': 'Weekend Flash Sale',
        'description': 'Get ₱500 off on all processors this weekend!',
        'deal_type': 'fixed',
        'discount_amount': 500,
        'badge_text': 'FLASH SALE',
        'is_featured': True,
        'status': 'active',
    },
    {
        'title': 'Buy 1 Get 1 Memory Deal',
        'description': 'Buy one RAM module, get another one free!',
        'deal_type': 'bogo',
        'badge_text': 'BOGO',
        'is_featured': False,
        'status': 'active',
    },
    {
        'title': 'Graphics Card Bundle',
        'description': 'Special bundle pricing on GPU + accessories',
        'deal_type': 'bundle',
        'discount_percentage': 15,
        'badge_text': 'BUNDLE',
        'is_featured': False,
        'status': 'active',
    },
]

now = timezone.now()
created_count = 0

for deal_data in deals_data:
    # Check if deal already exists
    if Deal.objects.filter(title=deal_data['title']).exists():
        print(f"⊘ Deal already exists: {deal_data['title']}")
        continue
    
    # Set dates
    deal_data['start_date'] = now
    deal_data['end_date'] = now + timedelta(days=7)
    deal_data['created_by'] = admin_user
    
    # Create deal
    deal = Deal.objects.create(**deal_data)
    
    # Add 3-5 random products to each deal
    deal_products = products[:5] if len(products) >= 5 else products
    deal.products.set(deal_products)
    
    # Apply deal to products
    deal.apply_to_products()
    
    print(f"✓ Created deal: {deal.title} ({deal_products.count()} products)")
    created_count += 1

print(f"\n🎉 Successfully created {created_count} sample deals!")
print(f"📊 Total active deals: {Deal.objects.filter(status='active').count()}")
print(f"🛍️ Products on sale: {Product.objects.filter(on_sale=True).count()}")
print("\n✓ You can now view deals at:")
print("   - Customer: http://127.0.0.1:8000/deals/")
print("   - Admin: http://127.0.0.1:8000/dashboard/deals/")
