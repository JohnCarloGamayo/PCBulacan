"""
Script to fix deal dates and statuses
Run: python manage.py shell < fix_deal_dates.py
"""
import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from django.utils import timezone
from products.models import Deal

now = timezone.now()
print(f"Current time (Manila): {now}")
print(f"=" * 60)

deals = Deal.objects.all()
fixed_count = 0

for deal in deals:
    print(f"\n📦 Deal: {deal.title}")
    print(f"   Status: {deal.status}")
    print(f"   Start: {deal.start_date}")
    print(f"   End: {deal.end_date}")
    print(f"   Is active (method): {deal.is_active()}")
    
    # Check if dates are valid
    if deal.start_date > deal.end_date:
        print(f"   ❌ ERROR: Start date is after end date!")
        # Fix: Set reasonable dates
        deal.start_date = now
        deal.end_date = now + timedelta(days=7)
        deal.save()
        print(f"   ✓ Fixed dates: {deal.start_date} to {deal.end_date}")
        fixed_count += 1
    
    # Check if status matches date logic
    should_be_active = deal.start_date <= now <= deal.end_date
    
    if should_be_active and deal.status != 'active':
        print(f"   ⚠️  Should be ACTIVE but status is: {deal.status}")
        if deal.status == 'expired':
            # If marked expired but should be active, fix it
            deal.status = 'active'
            deal.save()
            print(f"   ✓ Changed status to ACTIVE")
            fixed_count += 1
    elif not should_be_active and deal.status == 'active':
        print(f"   ⚠️  Marked ACTIVE but dates don't match")
        if deal.end_date < now:
            deal.status = 'expired'
            deal.save()
            print(f"   ✓ Changed status to EXPIRED")
            fixed_count += 1
        elif deal.start_date > now:
            deal.status = 'scheduled'
            deal.save()
            print(f"   ✓ Changed status to SCHEDULED")
            fixed_count += 1

print(f"\n{'=' * 60}")
print(f"🎉 Fixed {fixed_count} deals!")
print(f"\nCurrent deal stats:")
print(f"   Active: {Deal.objects.filter(status='active').count()}")
print(f"   Draft: {Deal.objects.filter(status='draft').count()}")
print(f"   Scheduled: {Deal.objects.filter(status='scheduled').count()}")
print(f"   Expired: {Deal.objects.filter(status='expired').count()}")
