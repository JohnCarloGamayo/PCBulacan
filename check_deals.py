"""Check current deals and their usage"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from products.models import Deal

print("Current Deals:")
print("="*60)
for deal in Deal.objects.all():
    max_uses_str = str(deal.max_uses) if deal.max_uses else "unlimited"
    print(f"{deal.title}")
    print(f"  Status: {deal.status}")
    print(f"  Usage: {deal.current_uses}/{max_uses_str}")
    print(f"  Products: {deal.products.count()}")
    print()
