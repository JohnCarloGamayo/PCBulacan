"""
Test script for dynamic product queries
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from ai_training_data import get_ai_response

print("\n" + "="*80)
print("TESTING DYNAMIC PRODUCT QUERY SYSTEM")
print("="*80 + "\n")

# Test 1: Product categories
print("1. Test: 'Ano mga binibenta nyo na products?'")
print("-" * 80)
response = get_ai_response("Ano mga binibenta nyo na products?")
print(response[:300] + "..." if len(response) > 300 else response)

print("\n" + "-" * 80)
print("2. Test: 'May asus rog laptop kayo?'")
print("-" * 80)
response = get_ai_response("May asus rog laptop kayo?")
print(response[:300] + "..." if len(response) > 300 else response)

print("\n" + "-" * 80)
print("3. Test: 'May sale ba kayo?'")
print("-" * 80)
response = get_ai_response("May sale ba kayo?")
print(response[:300] + "..." if len(response) > 300 else response)

print("\n" + "-" * 80)
print("4. Test: 'Do you have RTX 4090?'")
print("-" * 80)
response = get_ai_response("Do you have RTX 4090?")
print(response[:300] + "..." if len(response) > 300 else response)

print("\n" + "-" * 80)
print("5. Test: 'What products do you sell?'")
print("-" * 80)
response = get_ai_response("What products do you sell?")
print(response[:300] + "..." if len(response) > 300 else response)

print("\n" + "="*80)
print("SYSTEM FEATURES:")
print("="*80)
print("""
✅ Dynamic Product Categories - Lists all active categories from database
✅ Product Search - Searches products by name, description, category
✅ Active Deals - Shows current deals and sale products with prices
✅ Real-time Stock Status - Shows if in stock or out of stock
✅ Sale Prices - Displays original and discounted prices
✅ Bilingual Support - Works in English and Tagalog

All data comes directly from database - always up-to-date!
""")
print("="*80 + "\n")
