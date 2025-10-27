"""
Add sample delivery fees for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from orders.models import DeliveryFee

# Sample delivery fees for Bulacan and nearby areas
delivery_fees_data = [
    {'city': 'Malolos', 'state': 'Bulacan', 'fee_amount': 150.00, 'estimated_days': '3-5 days'},
    {'city': 'Meycauayan', 'state': 'Bulacan', 'fee_amount': 120.00, 'estimated_days': '3-5 days'},
    {'city': 'San Jose del Monte', 'state': 'Bulacan', 'fee_amount': 130.00, 'estimated_days': '3-5 days'},
    {'city': 'Pandi', 'state': 'Bulacan', 'fee_amount': 180.00, 'estimated_days': '4-6 days'},
    {'city': 'Balagtas', 'state': 'Bulacan', 'fee_amount': 160.00, 'estimated_days': '3-5 days'},
    {'city': 'Bocaue', 'state': 'Bulacan', 'fee_amount': 140.00, 'estimated_days': '3-5 days'},
    {'city': 'Caloocan', 'state': 'Metro Manila', 'fee_amount': 100.00, 'estimated_days': '2-3 days'},
    {'city': 'Manila', 'state': 'Metro Manila', 'fee_amount': 100.00, 'estimated_days': '2-3 days'},
    {'city': 'Quezon City', 'state': 'Metro Manila', 'fee_amount': 100.00, 'estimated_days': '2-3 days'},
    {'city': 'Valenzuela', 'state': 'Metro Manila', 'fee_amount': 100.00, 'estimated_days': '2-3 days'},
]

print("Adding delivery fees...")

for fee_data in delivery_fees_data:
    fee, created = DeliveryFee.objects.get_or_create(
        city=fee_data['city'],
        state=fee_data['state'],
        defaults={
            'fee_amount': fee_data['fee_amount'],
            'estimated_days': fee_data['estimated_days'],
            'is_available': True,
            'min_order_free_delivery': 5000.00
        }
    )
    if created:
        print(f"✓ Added: {fee.city}, {fee.state} - ₱{fee.fee_amount} ({fee.estimated_days})")
    else:
        print(f"  Already exists: {fee.city}, {fee.state} - ₱{fee.fee_amount}")

total_fees = DeliveryFee.objects.count()
print(f"\nTotal delivery fees in database: {total_fees}")
print("\nDelivery fees available:")
for fee in DeliveryFee.objects.all().order_by('state', 'city'):
    print(f"  • {fee.city}, {fee.state} - ₱{fee.fee_amount} ({fee.estimated_days})")

