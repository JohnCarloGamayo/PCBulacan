#!/usr/bin/env python
"""
Add default product categories for PCBulacan
Run this script to populate the database with initial categories
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from products.models import Category

# Default categories for PC components
categories = [
    {'name': 'Processors (CPU)', 'description': 'Computer processors from Intel and AMD'},
    {'name': 'Motherboards', 'description': 'Motherboards for Intel and AMD processors'},
    {'name': 'Graphics Cards (GPU)', 'description': 'NVIDIA and AMD graphics cards'},
    {'name': 'Memory (RAM)', 'description': 'DDR4 and DDR5 memory modules'},
    {'name': 'Storage', 'description': 'SSDs, HDDs, and NVMe drives'},
    {'name': 'Power Supply (PSU)', 'description': 'Power supplies for PC builds'},
    {'name': 'Cases', 'description': 'PC cases and chassis'},
    {'name': 'Cooling', 'description': 'CPU coolers, case fans, and liquid cooling'},
    {'name': 'Monitors', 'description': 'Gaming and professional monitors'},
    {'name': 'Keyboards', 'description': 'Mechanical and membrane keyboards'},
    {'name': 'Mouse', 'description': 'Gaming and office mice'},
    {'name': 'Headsets', 'description': 'Gaming headsets and audio devices'},
    {'name': 'Accessories', 'description': 'Cables, adapters, and other PC accessories'},
]

def add_categories():
    """Add default categories to database"""
    print("Adding categories to database...\n")
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✓ Created: {category.name}")
        else:
            print(f"→ Already exists: {category.name}")
    
    print(f"\n✅ Done! Total categories: {Category.objects.count()}")

if __name__ == '__main__':
    add_categories()
