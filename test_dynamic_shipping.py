"""
Test script to demonstrate dynamic shipping fee system
Shows that AI responses update automatically when database changes
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from ai_training_data import get_shipping_fees_from_db, get_ai_response
from orders.models import DeliveryFee

print("\n" + "="*80)
print("TESTING DYNAMIC SHIPPING FEE SYSTEM")
print("="*80 + "\n")

# Test 1: Show current shipping fees from database
print("1. Current shipping fees in database:")
print("-" * 80)
fees = DeliveryFee.objects.filter(is_available=True).order_by('state', 'city')
for fee in fees:
    free_text = f"(FREE @ P{fee.min_order_free_delivery:,.0f}+)" if fee.min_order_free_delivery > 0 else ""
    print(f"   {fee.city}, {fee.state}: P{fee.fee_amount:,.0f} {free_text}")

print("\n" + "-" * 80)
print("2. AI Response to 'How much is shipping?':")
print("-" * 80)
response = get_ai_response("How much is shipping?")
print(response)

print("\n" + "-" * 80)
print("3. AI Response to 'Magkano shipping fee?':")
print("-" * 80)
response = get_ai_response("Magkano shipping fee?")
print(response)

print("\n" + "="*80)
print("HOW IT WORKS:")
print("="*80)
print("""
When you update shipping fees in the admin dashboard:
1. Admin changes DeliveryFee data in database
2. AI chatbot automatically fetches new data via get_shipping_fees_from_db()
3. Customers see updated prices immediately - NO CODE CHANGES NEEDED!

Example scenario:
- Admin increases Malolos fee from P150 to P180
- Next customer asks "How much is shipping?"
- AI automatically responds with new P180 price

This is DYNAMIC - data comes directly from database, not hard-coded!
""")
print("="*80 + "\n")
