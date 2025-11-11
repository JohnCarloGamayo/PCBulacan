from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product


@login_required
def cart_view(request):
    """Display shopping cart and handle checkout with selected items"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Handle POST request (proceed to checkout with selected items)
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        if not selected_items:
            messages.error(request, 'Please select at least one item to checkout.')
            return redirect('orders:cart')
        
        # Save selected item IDs to session
        request.session['selected_cart_items'] = [int(item_id) for item_id in selected_items]
        return redirect('orders:checkout')
    
    context = {'cart': cart}
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Support both form POST and JSON POST
    if request.content_type == 'application/json':
        import json
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
        except Exception:
            quantity = 1
    else:
        quantity = int(request.POST.get('quantity', 1))
    
    if product.stock < quantity:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': 'Not enough stock available.'})
        messages.error(request, 'Not enough stock available.')
        return redirect('products:detail', slug=product.slug)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    if cart_item.quantity > product.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': 'Not enough stock available.'})
        messages.error(request, 'Not enough stock available.')
        return redirect('products:detail', slug=product.slug)
    
    cart_item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items
        })
    messages.success(request, f'{product.name} added to cart!')
    return redirect('orders:cart')


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({'success': True, 'item_total': 0, 'cart_subtotal': cart_item.cart.subtotal})
        elif quantity > cart_item.product.stock:
            return JsonResponse({'success': False, 'error': 'Not enough stock available.'})
        else:
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True, 'item_total': cart_item.total_price, 'cart_subtotal': cart_item.cart.subtotal})
    else:
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            if quantity > cart_item.product.stock:
                messages.error(request, 'Not enough stock available.')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated.')
        return redirect('orders:cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items
        })
    
    return redirect('orders:cart')


@login_required
def clear_cart(request):
    """Clear all items from cart"""
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        messages.success(request, 'Cart cleared successfully.')
    return redirect('orders:cart')


@login_required
def buy_now(request, product_id):
    """Buy now - go directly to checkout without modifying cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Support both form POST and JSON POST
    if request.content_type == 'application/json':
        import json
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
        except Exception:
            quantity = 1
    else:
        quantity = int(request.POST.get('quantity', 1))
    
    # Check stock
    if product.stock < quantity:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': 'Not enough stock available.'})
        messages.error(request, 'Not enough stock available.')
        return redirect('products:list')
    
    # Store buy now item in session (temporary, doesn't modify cart)
    request.session['buy_now_item'] = {
        'product_id': product.id,
        'quantity': quantity
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'redirect_url': '/orders/checkout/'
        })
    
    return redirect('orders:checkout')


@login_required
def checkout_view(request):
    """Checkout page with selected items or buy now item"""
    from accounts.models import UserAddress
    from decimal import Decimal
    from .models import DeliveryFee
    
    # Check if this is a buy now checkout (temporary item in session)
    buy_now_data = request.session.get('buy_now_item')
    
    if buy_now_data:
        # Buy now checkout - create temporary item data
        product = get_object_or_404(Product, id=buy_now_data['product_id'], is_active=True)
        
        # Create a temporary "item-like" object for the template
        class TempItem:
            def __init__(self, product, quantity):
                self.product = product
                self.quantity = quantity
                self.total_price = product.final_price * quantity
                self.total_savings = product.savings_amount * quantity
        
        selected_items = [TempItem(product, buy_now_data['quantity'])]
        is_buy_now = True
    else:
        # Regular cart checkout
        selected_item_ids = request.session.get('selected_cart_items', [])
        
        if not selected_item_ids:
            messages.error(request, 'Please select items to checkout.')
            return redirect('orders:cart')
        
        # Get cart and selected items
        cart = get_object_or_404(Cart, user=request.user)
        selected_items = cart.items.filter(id__in=selected_item_ids)
        
        if not selected_items.exists():
            messages.error(request, 'Selected items not found in cart.')
            return redirect('orders:cart')
        
        is_buy_now = False
    
    # Get user's addresses and attach delivery fee data
    addresses = UserAddress.objects.filter(user=request.user)
    
    # Attach delivery fee information to each address
    for address in addresses:
        try:
            delivery_fee = DeliveryFee.objects.get(
                city__iexact=address.city,
                state__iexact=address.state,
                is_available=True
            )
            address.delivery_fee = float(delivery_fee.fee_amount)
            address.min_order_free_delivery = float(delivery_fee.min_order_free_delivery)
            address.estimated_days = delivery_fee.estimated_days
        except DeliveryFee.DoesNotExist:
            # Default values if no delivery fee found
            address.delivery_fee = 0
            address.min_order_free_delivery = 0
            address.estimated_days = 'To be determined'
    
    # Calculate subtotal for selected items
    subtotal = Decimal(str(sum(item.total_price for item in selected_items)))
    
    if request.method == 'POST':
        # Get form data
        shipping_address_id = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        
        # Validate shipping address
        if not shipping_address_id:
            messages.error(request, 'Please select a shipping address.')
            return redirect('orders:checkout')
        
        shipping_address = get_object_or_404(UserAddress, id=shipping_address_id, user=request.user)
        
        # Calculate shipping cost based on delivery fee settings
        try:
            delivery_fee = DeliveryFee.objects.get(
                city__iexact=shipping_address.city,
                state__iexact=shipping_address.state,
                is_available=True
            )
            # Check if order qualifies for free delivery
            if subtotal >= delivery_fee.min_order_free_delivery and delivery_fee.min_order_free_delivery > 0:
                shipping_cost = Decimal('0.00')
            else:
                shipping_cost = delivery_fee.fee_amount
        except DeliveryFee.DoesNotExist:
            # Default shipping cost if no delivery fee found
            shipping_cost = Decimal('0.00')
        
        # Calculate total
        total = subtotal + shipping_cost
        
        # Handle payment screenshot for GCash and PayMaya
        payment_screenshot = None
        if payment_method in ['gcash', 'paymaya']:
            if 'payment_screenshot' in request.FILES:
                payment_screenshot = request.FILES['payment_screenshot']
            else:
                messages.error(request, f'Please upload payment screenshot for {payment_method.upper()}.')
                context = {
                    'selected_items': selected_items,
                    'addresses': addresses,
                    'subtotal': subtotal,
                    'is_buy_now': is_buy_now,
                }
                if not is_buy_now:
                    cart = Cart.objects.get(user=request.user)
                    context['cart'] = cart
                return render(request, 'orders/checkout.html', context)
        
        try:
            # Create order
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                full_name=f"{request.user.first_name} {request.user.last_name}",
                email=request.user.email,
                phone=getattr(request.user, 'phone', '') or '',
                address=shipping_address.address_line1,
                city=shipping_address.city,
                state=shipping_address.state,
                zip_code=shipping_address.postal_code,
                payment_method=payment_method,
                payment_screenshot=payment_screenshot,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                total=total,
            )
            
            # Create order items from selected cart items
            for item in selected_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.final_price  # Use discounted price
                )
                
                # Note: Stock will be deducted when order status is changed to 'shipped' by admin
            
            # Remove selected items from cart (only if not buy now)
            if not is_buy_now:
                selected_items.delete()
                # Clear selected items from session
                if 'selected_cart_items' in request.session:
                    del request.session['selected_cart_items']
            else:
                # Clear buy now item from session
                if 'buy_now_item' in request.session:
                    del request.session['buy_now_item']
            
            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('orders:order_confirmation', order_number=order.order_number)
            
        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
            return redirect('orders:checkout')
    
    # Calculate total for selected items
    if is_buy_now:
        total = Decimal(str(selected_items[0].total_price))  # For buy now, just one item
        total_savings = Decimal(str(selected_items[0].total_savings)) if hasattr(selected_items[0], 'total_savings') else Decimal('0')
    else:
        total = Decimal(str(sum(item.total_price for item in selected_items)))
        total_savings = Decimal(str(sum(item.total_savings for item in selected_items)))

    context = {
        'selected_items': selected_items,
        'addresses': addresses,
        'subtotal': total,  # Use the calculated total as subtotal
        'total': total,     # Initial total (before delivery fee)
        'total_savings': total_savings,
        'is_buy_now': is_buy_now,
    }
    
    # Only add cart to context if not buy now
    if not is_buy_now:
        cart = Cart.objects.get(user=request.user)
        context['cart'] = cart
    
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list_view(request):
    """Display user's orders"""
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'orders/order_list.html', context)


@login_required
def order_confirmation_view(request, order_number):
    """Order confirmation page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_confirmation.html', context)


@login_required
def order_detail_view(request, order_number):
    """Display order details"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)
