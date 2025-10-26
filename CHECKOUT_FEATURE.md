# Checkout Feature - PCBulacan

## Overview
Complete checkout system with selected cart items, multiple payment methods, and payment screenshot upload.

## Features Implemented

### 1. **Cart Selection & Checkout**
- ✅ Select individual items or "Select All" in cart
- ✅ Live order summary showing selected items and total
- ✅ "Proceed to Checkout" button (enabled only when items are selected)
- ✅ Selected items saved to session

### 2. **Checkout Page** (`/orders/checkout/`)
- ✅ Display selected items from cart
- ✅ Shipping address selection from user's saved addresses
- ✅ Add new address link to account page
- ✅ Order summary sidebar (sticky)

### 3. **Payment Methods**
- ✅ **Cash on Delivery (COD)** - No screenshot required
- ✅ **GCash** - Screenshot upload required
- ✅ **PayMaya** - Screenshot upload required

### 4. **Payment Screenshot Upload**
- ✅ Drag & drop or click to upload
- ✅ Image preview before submission
- ✅ View full-size image in modal
- ✅ Remove/change image
- ✅ File validation (5MB max, image types only)

### 5. **Order Confirmation** (`/orders/order-confirmation/<order_number>/`)
- ✅ Success message with order number
- ✅ Order details summary
- ✅ Shipping address display
- ✅ Order items table
- ✅ Payment verification notice (for GCash/PayMaya)
- ✅ Links to continue shopping or view orders

## Database Models Updated

### Order Model (`orders.models.py`)
```python
payment_method choices:
- 'cod': Cash on Delivery
- 'gcash': GCash
- 'paymaya': PayMaya

payment_screenshot: ImageField (optional, required for gcash/paymaya)
```

### UserAddress Model (`accounts.models.py`)
```python
label: CharField (e.g., 'Home', 'Office') - NEW
```

## Files Created/Modified

### Created:
1. `templates/orders/checkout.html` - Checkout page
2. `templates/orders/order_confirmation.html` - Confirmation page
3. `orders/migrations/0003_order_payment_screenshot_alter_order_payment_method.py`
4. `accounts/migrations/0004_useraddress_label.py`

### Modified:
1. `orders/views.py` - Added checkout_view, order_confirmation_view, updated cart_view
2. `orders/urls.py` - Added checkout and order_confirmation routes
3. `orders/models.py` - Updated payment choices and added payment_screenshot
4. `accounts/models.py` - Added label field to UserAddress
5. `templates/orders/cart.html` - Added selection logic and form submission

## User Flow

1. **Cart Page**
   - User selects items to checkout
   - Order summary updates in real-time
   - Click "Proceed to Checkout"

2. **Checkout Page**
   - Select shipping address (or add new one)
   - Choose payment method (COD, GCash, or PayMaya)
   - For GCash/PayMaya: Upload payment screenshot
   - Click "Place Order"

3. **Order Processing**
   - Order created in database
   - Order items linked to order
   - Product stock updated
   - Selected items removed from cart
   - Session cleared

4. **Order Confirmation**
   - Display success message
   - Show order number for reference
   - Display order details
   - For GCash/PayMaya: Show payment verification pending notice

## Payment Instructions

### GCash
- Send payment to: **09123456789**
- Include name and order reference
- Upload payment screenshot

### PayMaya
- Send payment to: **09123456789**
- Include name and order reference
- Upload payment screenshot

### COD
- Pay when you receive the order
- No screenshot required

## Admin Features
- View payment screenshots in admin panel
- Verify payments
- Update order status

## Testing Checklist
- [ ] Add items to cart
- [ ] Select items for checkout
- [ ] Test "Select All" functionality
- [ ] Proceed to checkout without address (should redirect to add address)
- [ ] Proceed to checkout with address
- [ ] Test COD payment (no screenshot)
- [ ] Test GCash payment (with screenshot upload)
- [ ] Test PayMaya payment (with screenshot upload)
- [ ] Verify screenshot upload validation (file type, size)
- [ ] Complete order and check confirmation page
- [ ] Verify order appears in account orders
- [ ] Check cart items are removed after checkout

## Notes
- Shipping cost calculation not yet implemented (set to ₱0.00)
- PayMongo API integration removed (using manual screenshot verification)
- All payment methods now work with screenshot proof (except COD)

## Next Steps (Optional)
1. Add shipping cost calculator based on address/location
2. Add email notification after order placement
3. Add SMS notification for order updates
4. Implement admin order management dashboard
5. Add order tracking feature
6. Add order cancellation for customers
7. Add invoice generation (PDF)
