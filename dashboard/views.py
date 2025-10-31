from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, F, Avg
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from accounts.models import User
from products.models import Product, Category
from orders.models import Order, DeliveryFee
import json


@staff_member_required
def dashboard_home(request):
    """Admin dashboard homepage with statistics"""
    from datetime import datetime, timedelta
    from django.db.models import Q
    
    # Get date range filter (default: last 7 days)
    date_range = request.GET.get('date_range', 'last7days')
    today = timezone.now().date()
    
    if date_range == 'today':
        start_date = today
        end_date = today
    elif date_range == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)
    elif date_range == 'last7days':
        start_date = today - timedelta(days=7)
        end_date = today
    elif date_range == 'last30days':
        start_date = today - timedelta(days=30)
        end_date = today
    elif date_range == 'thisMonth':
        start_date = today.replace(day=1)
        end_date = today
    elif date_range == 'lastMonth':
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1)
        end_date = last_day_last_month
    else:
        start_date = today - timedelta(days=7)
        end_date = today
    
    # Filter orders by date range
    orders_in_range = Order.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )
    
    # Statistics
    total_users = User.objects.count()
    total_products = Product.objects.filter(is_active=True).count()
    total_orders = orders_in_range.count()
    pending_orders = orders_in_range.filter(status='pending').count()
    
    # Sales calculation (consistent with sales analytics):
    # - COD orders only count when status is 'received' (already paid)
    # - Other payment methods count when not cancelled (pre-paid)
    revenue_orders = orders_in_range.filter(
        Q(payment_method='cod', status='received') |
        Q(~Q(payment_method='cod'), ~Q(status='cancelled'))
    )
    total_sales = revenue_orders.aggregate(total=Sum('total'))['total'] or 0
    
    # Low stock products
    low_stock_products = Product.objects.filter(stock__lt=10, is_active=True)
    
    # Products by category
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    )
    category_labels = [cat.name for cat in categories]
    category_data = [cat.product_count for cat in categories]
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_sales': total_sales,
        'low_stock_products': low_stock_products,
        'date_range': date_range,
        'start_date': start_date,
        'end_date': end_date,
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
    }
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def manage_users(request):
    """Manage users"""
    from datetime import datetime, timedelta
    from django.db.models import Count, Sum, Q
    
    users = User.objects.all().order_by('-date_joined')
    
    # Calculate statistics
    total_users = users.count()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_users_30days = users.filter(date_joined__gte=thirty_days_ago).count()
    active_users = users.filter(is_active=True).count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'new_users_30days': new_users_30days,
        'active_users': active_users,
    }
    return render(request, 'dashboard/manage_users.html', context)


@staff_member_required
def view_user(request, user_id):
    """View user details via AJAX"""
    user = get_object_or_404(User, id=user_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from orders.models import Order
        from django.db.models import Sum
        
        # Get user orders statistics
        user_orders = Order.objects.filter(user=user)
        total_orders = user_orders.count()
        total_spent = user_orders.aggregate(total=Sum('total'))['total'] or 0
        
        profile_picture_url = user.profile_picture.url if user.profile_picture else None
        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_active': user.is_active,
            'date_joined': user.date_joined.strftime('%B %d, %Y'),
            'last_login': user.last_login.strftime('%B %d, %Y at %I:%M %p') if user.last_login else None,
            'total_orders': total_orders,
            'total_spent': f'{total_spent:,.2f}',
            'profile_picture_url': profile_picture_url,
        })
    
    return redirect('dashboard:manage_users')


@staff_member_required
def delete_user(request, user_id):
    """Delete user via AJAX"""
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Don't allow deleting yourself
            if user.id == request.user.id:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'You cannot delete yourself!'})
                messages.error(request, 'You cannot delete yourself!')
                return redirect('dashboard:manage_users')
            
            # Don't allow deleting staff/admin users
            if user.is_staff or user.is_superuser:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Cannot delete admin users!'})
                messages.error(request, 'Cannot delete admin users!')
                return redirect('dashboard:manage_users')
            
            user_email = user.email
            user.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'User {user_email} deleted successfully!'})
            
            messages.success(request, f'User {user_email} deleted successfully!')
            return redirect('dashboard:manage_users')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            messages.error(request, f'Error deleting user: {str(e)}')
            return redirect('dashboard:manage_users')
    
    return redirect('dashboard:manage_users')


@staff_member_required
def toggle_user_status(request, user_id):
    """Activate/deactivate user"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.email} has been {status}.')
    return redirect('dashboard:manage_users')


@staff_member_required
def manage_products(request):
    """Manage products"""
    products = Product.objects.all().select_related('category').order_by('-created_at')
    categories = Category.objects.all().order_by('name')
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'dashboard/manage_products_new.html', context)


@staff_member_required
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        try:
            # Validate required fields
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock', 0)
            
            if not category_id or not name or not price:
                raise ValueError('Category, Name, and Price are required.')
            
            # Handle SKU - convert empty string to None for unique constraint
            sku = request.POST.get('sku', '').strip()
            sku = sku if sku else None
            
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(
                category=category,
                name=name,
                description=request.POST.get('description', ''),
                price=price,
                old_price=request.POST.get('old_price') or None,
                stock=stock,
                sku=sku,
                image=request.FILES.get('image'),
                is_featured=request.POST.get('is_featured') == 'on',
                is_new=request.POST.get('is_new') == 'on',
                on_sale=request.POST.get('on_sale') == 'on',
            )
            
            # Handle additional images
            additional_images = request.FILES.getlist('additional_images')
            for index, image_file in enumerate(additional_images, start=1):
                from products.models import ProductImage
                ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    order=index,
                    is_primary=False
                )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Product added successfully',
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'stock': product.stock
                    }
                })
            
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('dashboard:manage_products')
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print("Error adding product:")
            print(error_details)  # Log to console without f-string
            error_message = 'Error adding product: ' + str(e)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            messages.error(request, error_message)
            return redirect('dashboard:manage_products')
    
    # For non-POST requests (shouldn't happen with AJAX modal)
    return redirect('dashboard:manage_products')


@staff_member_required
def edit_product(request, product_id):
    """Edit product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'GET':
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Get existing additional images
            from products.models import ProductImage
            additional_images = ProductImage.objects.filter(product=product).order_by('order')
            
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'category_id': product.category.id if product.category else None,
                'price': float(product.price),
                'stock': product.stock,
                'sku': product.sku or '',
                'description': product.description or '',
                'image': product.image.url if product.image else None,
                'additional_images': [{'id': img.id, 'url': img.image.url, 'order': img.order} for img in additional_images],
                'is_featured': product.is_featured,
                'is_new': product.is_new,
                'on_sale': product.on_sale,
            })
    
    if request.method == 'POST':
        try:
            # Handle SKU - convert empty string to None for unique constraint
            sku = request.POST.get('sku', '').strip()
            sku = sku if sku else None
            
            product.category = Category.objects.get(id=request.POST.get('category'))
            product.name = request.POST.get('name')
            product.description = request.POST.get('description', '')
            product.price = request.POST.get('price')
            product.old_price = request.POST.get('old_price') or None
            product.stock = request.POST.get('stock', 0)
            product.sku = sku
            product.is_featured = request.POST.get('is_featured') == 'on'
            product.is_new = request.POST.get('is_new') == 'on'
            product.on_sale = request.POST.get('on_sale') == 'on'
            product.is_active = request.POST.get('is_active', 'on') == 'on'
            
            if request.FILES.get('image'):
                product.image = request.FILES.get('image')
            
            product.save()
            
            # Handle additional images
            additional_images = request.FILES.getlist('additional_images')
            if additional_images:
                from products.models import ProductImage
                # Get current max order
                current_max = ProductImage.objects.filter(product=product).count()
                for index, image_file in enumerate(additional_images, start=current_max + 1):
                    ProductImage.objects.create(
                        product=product,
                        image=image_file,
                        order=index,
                        is_primary=False
                    )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Product updated successfully',
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'stock': product.stock
                    }
                })
            
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('dashboard:manage_products')
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print("Error editing product:")
            print(error_details)  # Log to console without f-string
            error_message = 'Error editing product: ' + str(e)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            messages.error(request, error_message)
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            messages.error(request, f'Error updating product: {str(e)}')
    
    categories = Category.objects.filter(is_active=True)
    context = {'product': product, 'categories': categories}
    return render(request, 'dashboard/edit_product.html', context)


@staff_member_required
def inventory_management(request):
    """Admin inventory management page (modern UI, filters, stock update)"""
    from django.db.models import Q

    # Handle stock update POST (add stock, not replace)
    if request.method == 'POST' and request.POST.get('product_id'):
        product_id = request.POST.get('product_id')
        try:
            add_stock = int(request.POST.get('add_stock', 0))
            if add_stock < 1:
                messages.error(request, "Please enter a valid quantity to add (minimum 1).")
                return redirect(request.path_info)
            
            product = Product.objects.get(id=product_id)
            old_stock = product.stock
            product.stock += add_stock
            product.save()
            messages.success(request, f"Added {add_stock} units to {product.name}. Stock updated from {old_stock} to {product.stock}.")
            return redirect(request.path_info)
        except Exception as e:
            messages.error(request, f"Error adding stock: {e}")

    # Filters
    search = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '')
    stock_status = request.GET.get('stock_status', '')
    sort_by = request.GET.get('sort_by', 'name')

    products = Product.objects.all()
    categories = Category.objects.filter(is_active=True)

    if search:
        products = products.filter(name__icontains=search)
    if category_id:
        products = products.filter(category_id=category_id)
    if stock_status == 'in_stock':
        products = products.filter(stock__gt=10)
    elif stock_status == 'low_stock':
        products = products.filter(stock__gt=0, stock__lte=10)
    elif stock_status == 'out_of_stock':
        products = products.filter(stock=0)

    # Sorting
    if sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'stock':
        products = products.order_by('stock')
    elif sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'created_at':
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'search': search,
        'category_id': category_id,
        'stock_status': stock_status,
        'sort_by': sort_by,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Render only the table wrapper for AJAX
        from django.template.loader import render_to_string
        table_html = render_to_string('dashboard/inventory_management.html', context, request=request)
        # Only return the table wrapper div
        import re
        match = re.search(r'<div class="inventory-table-wrapper"[\s\S]*?</div>\s*</div>', table_html)
        if match:
            return HttpResponse(match.group(0))
        return HttpResponse(table_html)
    return render(request, 'dashboard/inventory_management.html', context)


@staff_member_required
def delete_product(request, product_id):
    """Delete product"""
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            product_name = product.name
            product.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Product "{product_name}" deleted successfully'})
            
            messages.success(request, f'Product "{product_name}" deleted successfully!')
            return redirect('dashboard:manage_products')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            messages.error(request, f'Error deleting product: {str(e)}')
            return redirect('dashboard:manage_products')
    
    return redirect('dashboard:manage_products')


@staff_member_required
def delete_product_image(request, image_id):
    """Delete product image"""
    if request.method == 'POST':
        try:
            from products.models import ProductImage
            image = get_object_or_404(ProductImage, id=image_id)
            image.delete()
            
            return JsonResponse({'success': True, 'message': 'Image deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@staff_member_required
def manage_orders(request):
    """Manage orders with filtering"""
    orders = Order.objects.all().select_related('user')
    
    # Apply filters
    status_filter = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)
    
    if search:
        from django.db.models import Q
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(full_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    orders = orders.order_by('-created_at')
    
    context = {'orders': orders}
    return render(request, 'dashboard/manage_orders.html', context)


@staff_member_required
def order_details(request, order_number):
    """Get order details as JSON"""
    order = get_object_or_404(Order, order_number=order_number)
    
    items = []
    for item in order.items.all():
        items.append({
            'product_name': item.product.name,
            'price': str(item.price),
            'quantity': item.quantity,
            'total': str(item.total)
        })
    
    data = {
        'success': True,
        'order': {
            'order_number': order.order_number,
            'created_at': order.created_at.strftime('%B %d, %Y %I:%M %p'),
            'status': order.status,
            'status_display': order.get_status_display(),
            'payment_method': order.payment_method,
            'full_name': order.full_name,
            'email': order.email,
            'phone': order.phone or '',
            'address': order.address,
            'city': order.city,
            'state': order.state,
            'zip_code': order.zip_code,
            'items': items,
            'subtotal': str(order.subtotal),
            'shipping_cost': str(order.shipping_cost),
            'total': str(order.total),
            'payment_screenshot': order.payment_screenshot.url if order.payment_screenshot else None
        }
    }
    
    return JsonResponse(data)


@staff_member_required
def update_order_status(request, order_number):
    """Update order status with validation and email notification"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        old_status = order.status
        
        # Define valid status transitions
        valid_transitions = {
            'pending': ['processing', 'cancelled'],
            'processing': ['shipped'],
            'shipped': ['delivered'],
            'delivered': [],  # Customer confirms to 'received'
            'cancelled': [],
            'received': []
        }
        
        # Validate status transition
        if new_status not in valid_transitions.get(old_status, []):
            messages.error(request, f'Cannot change status from {old_status} to {new_status}. Invalid transition.')
            return redirect('dashboard:manage_orders')
        
        # If status is being changed to shipped, decrease product stock, mark shipped, then send email with PDF receipt
        if old_status != 'shipped' and new_status == 'shipped':
            # Decrease stock
            for item in order.items.all():
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()
                else:
                    messages.warning(request, f'Not enough stock for {product.name}. Only {product.stock} left.')
                    return redirect('dashboard:manage_orders')

            # Mark order as shipped first so PDF reflects new status
            order.status = new_status
            order.save()

            # Send email with PDF receipt
            try:
                from django.core.mail import EmailMessage
                from orders.pdf_generator import generate_order_receipt_pdf
                
                print(f"DEBUG: Starting email send for order {order.order_number}")
                print(f"DEBUG: Customer email: {order.email}")

                # Generate PDF (now order.status is 'shipped')
                pdf_content = generate_order_receipt_pdf(order)
                print(f"DEBUG: PDF generated successfully, size: {len(pdf_content)} bytes")

                # Create email
                subject = f'Your Order #{order.order_number} Has Been Shipped!'
                message = (
                    f"Dear {order.full_name},\n\n"
                    f"Good news — your order is on the way!\n\n"
                    f"Order Number: #{order.order_number}\n"
                    f"Total Amount: ₱{order.total:,.2f}\n"
                    f"Shipping Address: {order.address}, {order.city}, {order.state} {order.zip_code}\n\n"
                    "We've attached your official receipt to this email.\n"
                    "You can also check your order status in your account.\n\n"
                    "Thank you for shopping with PCBulacan!\n"
                    "Best regards,\nPCBulacan Team"
                )

                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email='PCBulacan <johncarlogamayo@gmail.com>',
                    to=[order.email],
                )

                # Attach PDF
                email.attach(
                    f'PCBulacan_Receipt_{order.order_number}.pdf',
                    pdf_content,
                    'application/pdf'
                )
                print(f"DEBUG: Email object created with attachment")

                # Send email
                result = email.send(fail_silently=False)
                print(f"DEBUG: Email sent! Result: {result}")
                messages.success(request, f'Order {order.order_number} marked as shipped — email with receipt sent to {order.email}.')

            except Exception as e:
                print(f"DEBUG: Email error: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                messages.warning(request, f'Order marked as shipped but failed to send email: {str(e)}')

        else:
            # Update order status for non-shipped transitions
            order.status = new_status
            order.save()
            messages.success(request, f'Order {order.order_number} status updated to {order.get_status_display()}.')
    
    return redirect('dashboard:manage_orders')


@staff_member_required
def manage_categories(request):
    """Manage categories"""
    categories = Category.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'dashboard/manage_categories.html', context)


@staff_member_required
def add_category(request):
    """Add new category"""
    if request.method == 'POST':
        try:
            category = Category.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                image=request.FILES.get('image'),
            )
            messages.success(request, f'Category "{category.name}" added successfully!')
            return redirect('dashboard:manage_categories')
        except Exception as e:
            messages.error(request, f'Error adding category: {str(e)}')
    
    return render(request, 'dashboard/add_category.html')


@staff_member_required
def manage_delivery_fees(request):
    """Manage delivery fees"""
    from django.db.models import Avg
    
    # Get statistics
    total_locations = DeliveryFee.objects.count()
    active_locations = DeliveryFee.objects.filter(is_available=True).count()
    avg_fee = DeliveryFee.objects.aggregate(avg=Avg('fee_amount'))['avg'] or 0
    free_delivery_locations = DeliveryFee.objects.filter(min_order_free_delivery__gt=0).count()
    
    # Get all delivery fees
    delivery_fees = DeliveryFee.objects.all().order_by('-id')
    
    # Get unique states for filter
    states = DeliveryFee.objects.values_list('state', flat=True).distinct().order_by('state')
    
    context = {
        'delivery_fees': delivery_fees,
        'total_locations': total_locations,
        'active_locations': active_locations,
        'avg_fee': avg_fee,
        'free_delivery_locations': free_delivery_locations,
        'states': states,
    }
    return render(request, 'dashboard/manage_delivery_fees.html', context)


@staff_member_required
def add_delivery_fee(request):
    """Add new delivery fee via AJAX"""
    if request.method == 'POST':
        try:
            city = request.POST.get('city')
            state = request.POST.get('state')
            fee_amount = request.POST.get('fee_amount')
            min_order = request.POST.get('min_order', 0)
            estimated_days = request.POST.get('estimated_days')
            is_available = request.POST.get('status') == 'Active'
            
            # Check if already exists
            if DeliveryFee.objects.filter(city=city, state=state).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'A delivery fee for this city and state already exists.'
                })
            
            delivery_fee = DeliveryFee.objects.create(
                city=city,
                state=state,
                fee_amount=fee_amount,
                min_order_free_delivery=min_order,
                estimated_days=estimated_days,
                is_available=is_available
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Delivery fee added successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error adding delivery fee: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@staff_member_required
def edit_delivery_fee(request, fee_id):
    """Edit delivery fee via AJAX"""
    delivery_fee = get_object_or_404(DeliveryFee, id=fee_id)
    
    if request.method == 'POST':
        try:
            delivery_fee.city = request.POST.get('city')
            delivery_fee.state = request.POST.get('state')
            delivery_fee.fee_amount = request.POST.get('fee_amount')
            delivery_fee.min_order_free_delivery = request.POST.get('min_order', 0)
            delivery_fee.estimated_days = request.POST.get('estimated_days')
            delivery_fee.is_available = request.POST.get('status') == 'Active'
            delivery_fee.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Delivery fee updated successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error updating delivery fee: {str(e)}'
            })
    
    # GET request - return fee data
    return JsonResponse({
        'id': delivery_fee.id,
        'city': delivery_fee.city,
        'state': delivery_fee.state,
        'fee_amount': str(delivery_fee.fee_amount),
        'min_order': str(delivery_fee.min_order_free_delivery),
        'estimated_days': delivery_fee.estimated_days,
        'status': 'Active' if delivery_fee.is_available else 'Inactive'
    })


@staff_member_required
def delete_delivery_fee(request, fee_id):
    """Delete delivery fee via AJAX"""
    if request.method == 'POST':
        try:
            delivery_fee = get_object_or_404(DeliveryFee, id=fee_id)
            delivery_fee.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Delivery fee deleted successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error deleting delivery fee: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@staff_member_required
def toggle_delivery_fee_status(request, fee_id):
    """Toggle delivery fee status via AJAX"""
    if request.method == 'POST':
        try:
            delivery_fee = get_object_or_404(DeliveryFee, id=fee_id)
            new_status = request.POST.get('status') == '1'
            delivery_fee.is_available = new_status
            delivery_fee.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Status updated successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error updating status: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@staff_member_required
def sales_analytics(request):
    """Sales analytics page with comprehensive reports"""
    from django.db.models import Q, Sum, Count, Avg, F
    from datetime import datetime, timedelta
    from orders.models import Order, OrderItem
    
    # Get filter parameters
    date_range = request.GET.get('date_range', 'last30days')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Set date range based on selection
    today = timezone.now().date()
    
    if date_range == 'today':
        start_date = today
        end_date = today
    elif date_range == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)
    elif date_range == 'last7days':
        start_date = today - timedelta(days=7)
        end_date = today
    elif date_range == 'last30days':
        start_date = today - timedelta(days=30)
        end_date = today
    elif date_range == 'thismonth':
        start_date = today.replace(day=1)
        end_date = today
    elif date_range == 'lastmonth':
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)
        start_date = first_day_last_month
        end_date = last_day_last_month
    elif date_range == 'thisyear':
        start_date = today.replace(month=1, day=1)
        end_date = today
    elif date_range == 'lastyear':
        start_date = (today.replace(month=1, day=1) - timedelta(days=1)).replace(month=1, day=1)
        end_date = today.replace(month=1, day=1) - timedelta(days=1)
    elif date_range == 'custom' and start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        start_date = today - timedelta(days=30)
        end_date = today
    
    # Get orders in date range (exclude cancelled orders)
    orders = Order.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).exclude(status='cancelled')
    
    # For revenue calculation: 
    # - COD orders only count when status is 'received'
    # - Other payment methods count when not cancelled
    revenue_orders = orders.filter(
        Q(payment_method='cod', status='received') |
        Q(~Q(payment_method='cod'), ~Q(status='cancelled'))
    )
    
    # Summary statistics
    total_orders = orders.count()
    total_revenue = revenue_orders.aggregate(total=Sum('total'))['total'] or 0
    total_subtotal = revenue_orders.aggregate(total=Sum('subtotal'))['total'] or 0
    total_shipping = total_revenue - total_subtotal
    average_order_value = revenue_orders.aggregate(avg=Avg('total'))['avg'] or 0
    unique_customers = orders.values('user').distinct().count()
    
    # Total sales excluding pending orders
    total_sales = revenue_orders.exclude(
        status='pending'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Sales by date for chart (only count revenue orders)
    sales_by_date = revenue_orders.values('created_at__date').annotate(
        order_count=Count('id'),
        daily_revenue=Sum('total')
    ).order_by('created_at__date')
    
    dates = [item['created_at__date'].strftime('%b %d') for item in sales_by_date]
    revenues = [float(item['daily_revenue']) for item in sales_by_date]
    
    # Sales by payment method (only count revenue orders)
    payment_methods = revenue_orders.values('payment_method').annotate(
        order_count=Count('id'),
        total_revenue=Sum('total')
    ).order_by('-total_revenue')
    
    payment_method_labels = [pm['payment_method'].replace('_', ' ').title() for pm in payment_methods]
    payment_method_data = [float(pm['total_revenue']) for pm in payment_methods]
    
    # Top selling products (only from revenue orders)
    top_products = OrderItem.objects.filter(
        order__created_at__date__gte=start_date,
        order__created_at__date__lte=end_date,
        order__in=revenue_orders
    ).values('product__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('-total_revenue')[:10]
    
    # Rename the key for template usage
    top_products = [
        {
            'product_name': item['product__name'],
            'total_quantity': item['total_quantity'],
            'total_revenue': item['total_revenue']
        }
        for item in top_products
    ]
    
    # Sales by status (only count revenue orders)
    statuses = revenue_orders.values('status').annotate(
        order_count=Count('id'),
        total_revenue=Sum('total')
    ).order_by('-total_revenue')
    
    status_labels = [s['status'].title() for s in statuses]
    status_data = [float(s['total_revenue']) for s in statuses]
    
    # Customer purchase frequency
    customer_frequency = orders.values('user').annotate(
        purchase_count=Count('id')
    ).values('purchase_count').annotate(
        customer_count=Count('user')
    ).order_by('purchase_count')
    
    frequency_labels = [f"{cf['purchase_count']} order(s)" for cf in customer_frequency]
    frequency_data = [cf['customer_count'] for cf in customer_frequency]
    
    context = {
        'date_range': date_range,
        'start_date': start_date,
        'end_date': end_date,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_sales': total_sales,
        'total_subtotal': total_subtotal,
        'total_shipping': total_shipping,
        'average_order_value': average_order_value,
        'unique_customers': unique_customers,
        'sales_by_date': sales_by_date,
        'dates': json.dumps(dates),
        'revenues': json.dumps(revenues),
        'payment_methods': payment_methods,
        'payment_method_labels': json.dumps(payment_method_labels),
        'payment_method_data': json.dumps(payment_method_data),
        'top_products': top_products,
        'statuses': statuses,
        'status_labels': json.dumps(status_labels),
        'status_data': json.dumps(status_data),
        'customer_frequency': customer_frequency,
        'frequency_labels': json.dumps(frequency_labels),
        'frequency_data': json.dumps(frequency_data),
    }
    
    return render(request, 'dashboard/sales_analytics.html', context)


@staff_member_required
def payment_history(request):
    """Payment history page with filtering and detailed payment tracking"""
    from django.db.models import Q, Sum, Count
    from django.core.paginator import Paginator
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    payment_method = request.GET.get('payment_method', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'date_desc')
    
    # Base queryset
    orders = Order.objects.select_related('user').all()
    
    # Apply filters
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if payment_method:
        orders = orders.filter(payment_method=payment_method)
    
    if date_from:
        from datetime import datetime
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        orders = orders.filter(created_at__date__gte=date_from_obj)
    
    if date_to:
        from datetime import datetime
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
        orders = orders.filter(created_at__date__lte=date_to_obj)
    
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(user__email__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    # Apply sorting
    if sort == 'date_asc':
        orders = orders.order_by('created_at')
    elif sort == 'amount_desc':
        orders = orders.order_by('-total')
    elif sort == 'amount_asc':
        orders = orders.order_by('total')
    else:  # date_desc (default)
        orders = orders.order_by('-created_at')
    
    # Get summary statistics (consistent with sales analytics)
    all_orders = Order.objects.all()
    
    # Revenue calculation (consistent logic):
    # - COD orders only count when status is 'received'
    # - Other payment methods count when not cancelled
    revenue_orders = all_orders.filter(
        Q(payment_method='cod', status='received') |
        Q(~Q(payment_method='cod'), ~Q(status='cancelled'))
    )
    
    summary = {
        'total_payments': all_orders.count(),
        'total_amount': revenue_orders.aggregate(total=Sum('total'))['total'] or 0,
        'completed_count': all_orders.filter(
            status__in=['shipped', 'delivered', 'received']
        ).count(),
        'completed_amount': all_orders.filter(
            status__in=['shipped', 'delivered', 'received']
        ).filter(
            Q(payment_method='cod', status='received') |
            Q(~Q(payment_method='cod'))
        ).aggregate(total=Sum('total'))['total'] or 0,
        'pending_count': all_orders.filter(status='pending').count(),
        'pending_amount': all_orders.filter(
            status='pending'
        ).exclude(payment_method='cod').aggregate(total=Sum('total'))['total'] or 0,
        'failed_count': all_orders.filter(status='cancelled').count(),
        'failed_amount': 0,  # Cancelled orders don't count towards revenue
    }
    
    # Get unique statuses and payment methods for filters
    statuses = Order.objects.values_list('status', flat=True).distinct().order_by('status')
    payment_methods = Order.objects.values_list('payment_method', flat=True).distinct().order_by('payment_method')
    
    # Pagination
    paginator = Paginator(orders, 10)  # 10 orders per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'summary': summary,
        'statuses': statuses,
        'payment_methods': payment_methods,
        'status_filter': status_filter,
        'payment_method': payment_method,
        'date_from': date_from,
        'date_to': date_to,
        'search': search,
        'sort': sort,
        'page_obj': page_obj,
    }
    
    return render(request, 'dashboard/payment_history.html', context)


@staff_member_required
def payment_details_json(request, order_number):
    """Get payment details as JSON"""
    try:
        order = get_object_or_404(Order, order_number=order_number)

        # Get customer info robustly
        user = getattr(order, 'user', None)
        full_name = getattr(order, 'full_name', '') or ''
        email = getattr(order, 'email', '') or ''
        phone = getattr(order, 'phone', '') or ''
        customer = {
            'name': (f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip() if user else full_name) or full_name,
            'email': getattr(user, 'email', None) or email,
            'phone': phone
        }

        # Get shipping address robustly
        shipping_address_obj = getattr(order, 'shipping_address', None)
        shipping_address = {
            'address': getattr(shipping_address_obj, 'address', None) or getattr(order, 'address', '') or '',
            'city': getattr(shipping_address_obj, 'city', None) or getattr(order, 'city', '') or '',
            'state': getattr(shipping_address_obj, 'state', None) or getattr(order, 'state', '') or '',
            'zip_code': getattr(shipping_address_obj, 'zip_code', None) or getattr(order, 'zip_code', '') or ''
        }

        # Get order items robustly
        items = []
        for item in order.items.all():
            items.append({
                'product_name': getattr(item.product, 'name', ''),
                'price': str(getattr(item, 'price', 0)),
                'quantity': getattr(item, 'quantity', 0),
                'total': str(getattr(item, 'total', 0)),
            })

        # Build response data (match PHP structure)
        data = {
            'success': True,
            'order': {
                'order_number': getattr(order, 'order_number', ''),
                'created_at': order.created_at.strftime('%B %d, %Y at %I:%M %p') if getattr(order, 'created_at', None) else '',
                'status': getattr(order, 'status', ''),
                'status_display': order.get_status_display() if hasattr(order, 'get_status_display') else '',
                'payment_method': getattr(order, 'payment_method', ''),
                'payment_method_display': order.get_payment_method_display() if hasattr(order, 'get_payment_method_display') else '',
                'customer': customer,
                'shipping_address': shipping_address,
                'items': items,
                'subtotal': str(getattr(order, 'subtotal', 0)),
                'shipping_cost': str(getattr(order, 'shipping_cost', 0)),
                'total': str(getattr(order, 'total', 0)),
                'payment_screenshot': order.payment_screenshot.url if getattr(order, 'payment_screenshot', None) else ''
            }
        }
        return JsonResponse(data)
    except Exception as e:
        import sys
        print('PAYMENT DETAILS ERROR:', str(e), file=sys.stderr)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
def dashboard_sales_data(request):
    """Get sales data for dashboard chart"""
    from datetime import datetime, timedelta
    from django.db.models import Q
    
    date_range = request.GET.get('date_range', 'last7days')
    today = timezone.now().date()
    
    if date_range == 'today':
        start_date = today
        end_date = today
        days = 1
    elif date_range == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)
        days = 1
    elif date_range == 'last7days':
        start_date = today - timedelta(days=6)
        end_date = today
        days = 7
    elif date_range == 'last30days':
        start_date = today - timedelta(days=29)
        end_date = today
        days = 30
    elif date_range == 'thisMonth':
        start_date = today.replace(day=1)
        end_date = today
        days = (end_date - start_date).days + 1
    elif date_range == 'lastMonth':
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1)
        end_date = last_day_last_month
        days = (end_date - start_date).days + 1
    else:
        start_date = today - timedelta(days=6)
        end_date = today
        days = 7
    
    # Generate labels and data for each day
    labels = []
    data = []
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        labels.append(current_date.strftime('%b %d'))
        
        # Get sales for this day (consistent revenue logic)
        # COD orders only count when received, others when not cancelled
        daily_orders = Order.objects.filter(created_at__date=current_date)
        revenue_orders = daily_orders.filter(
            Q(payment_method='cod', status='received') |
            Q(~Q(payment_method='cod'), ~Q(status='cancelled'))
        )
        daily_sales = revenue_orders.aggregate(total=Sum('total'))['total'] or 0
        
        data.append(float(daily_sales))
    
    return JsonResponse({
        'labels': labels,
        'data': data
    })


@staff_member_required
def dashboard_recent_orders(request):
    """Get recent orders for dashboard"""
    orders = Order.objects.all().order_by('-created_at')[:10]
    
    orders_data = []
    for order in orders:
        orders_data.append({
            'order_number': order.order_number,
            'customer': order.full_name,
            'amount': str(order.total),
            'status': order.status,
            'status_display': order.get_status_display(),
            'date': order.created_at.strftime('%b %d, %Y'),
        })
    
    return JsonResponse({'orders': orders_data})


@staff_member_required
def dashboard_top_products(request):
    """Get top selling products for dashboard"""
    from orders.models import OrderItem
    from django.db.models import Q
    
    date_range = request.GET.get('date_range', 'last7days')
    today = timezone.now().date()
    
    if date_range == 'today':
        start_date = today
    elif date_range == 'yesterday':
        start_date = today - timedelta(days=1)
    elif date_range == 'last7days':
        start_date = today - timedelta(days=7)
    elif date_range == 'last30days':
        start_date = today - timedelta(days=30)
    elif date_range == 'thisMonth':
        start_date = today.replace(day=1)
    elif date_range == 'lastMonth':
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1)
    else:
        start_date = today - timedelta(days=7)
    
    # Get top products by quantity sold (consistent revenue logic)
    # Only count from orders that qualify as revenue
    top_products = OrderItem.objects.filter(
        order__created_at__date__gte=start_date
    ).filter(
        Q(order__payment_method='cod', order__status='received') |
        Q(~Q(order__payment_method='cod'), ~Q(order__status='cancelled'))
    ).values(
        'product__name',
        'product__category__name'
    ).annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('-total_sold')[:10]
    
    products_data = []
    for item in top_products:
        products_data.append({
            'name': item['product__name'],
            'category': item['product__category__name'] or 'Uncategorized',
            'sold': item['total_sold'],
            'revenue': str(item['total_revenue'])
        })
    
    return JsonResponse({'products': products_data})


@staff_member_required
def admin_account(request):
    """Admin account settings page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate email matches current user
        if email != request.user.email:
            messages.error(request, 'Email address does not match your account.')
            return redirect('dashboard:admin_account')
        
        # Verify current password
        from django.contrib.auth import authenticate
        user = authenticate(username=request.user.username, password=current_password)
        if user is None:
            messages.error(request, 'Current password is incorrect.')
            return redirect('dashboard:admin_account')
        
        # Validate new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('dashboard:admin_account')
        
        # Validate password strength
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('dashboard:admin_account')
        
        # Check if password has uppercase, lowercase, and number
        has_upper = any(c.isupper() for c in new_password)
        has_lower = any(c.islower() for c in new_password)
        has_digit = any(c.isdigit() for c in new_password)
        
        if not (has_upper and has_lower and has_digit):
            messages.error(request, 'Password must contain at least one uppercase letter, one lowercase letter, and one number.')
            return redirect('dashboard:admin_account')
        
        # Update password
        try:
            request.user.set_password(new_password)
            request.user.save()
            
            # Re-authenticate user to maintain session
            from django.contrib.auth import login
            user = authenticate(username=request.user.username, password=new_password)
            if user:
                login(request, user)
            
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard:admin_account')
        except Exception as e:
            messages.error(request, f'Error changing password: {str(e)}')
            return redirect('dashboard:admin_account')
    
    return render(request, 'dashboard/admin_account.html')


@staff_member_required
def manage_slideshow(request):
    """Manage homepage slideshow images"""
    from .models import SlideshowImage
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            title = request.POST.get('title')
            slide_type = request.POST.get('slide_type', 'main')
            link = request.POST.get('link', '')
            order = request.POST.get('order', 0)
            image = request.FILES.get('image')
            
            if title and image:
                SlideshowImage.objects.create(
                    title=title,
                    image=image,
                    slide_type=slide_type,
                    link=link,
                    order=order
                )
                messages.success(request, f'Slideshow image "{title}" added successfully!')
            else:
                messages.error(request, 'Please provide a title and image.')
            
            return redirect('dashboard:manage_slideshow')
        
        elif action == 'edit':
            slide_id = request.POST.get('slide_id')
            slide = get_object_or_404(SlideshowImage, id=slide_id)
            
            slide.title = request.POST.get('title', slide.title)
            slide.slide_type = request.POST.get('slide_type', slide.slide_type)
            slide.link = request.POST.get('link', '')
            slide.order = request.POST.get('order', slide.order)
            
            if 'image' in request.FILES:
                slide.image = request.FILES['image']
            
            slide.save()
            messages.success(request, f'Slideshow image "{slide.title}" updated successfully!')
            return redirect('dashboard:manage_slideshow')
        
        elif action == 'delete':
            slide_id = request.POST.get('slide_id')
            slide = get_object_or_404(SlideshowImage, id=slide_id)
            title = slide.title
            slide.delete()
            messages.success(request, f'Slideshow image "{title}" deleted successfully!')
            return redirect('dashboard:manage_slideshow')
        
        elif action == 'toggle':
            slide_id = request.POST.get('slide_id')
            slide = get_object_or_404(SlideshowImage, id=slide_id)
            slide.is_active = not slide.is_active
            slide.save()
            status = 'activated' if slide.is_active else 'deactivated'
            messages.success(request, f'Slideshow image "{slide.title}" {status} successfully!')
            return redirect('dashboard:manage_slideshow')
    
    # Get all slideshow images
    main_slides = SlideshowImage.objects.filter(slide_type='main')
    banner_slides = SlideshowImage.objects.filter(slide_type='banner')
    
    context = {
        'main_slides': main_slides,
        'banner_slides': banner_slides,
    }
    
    return render(request, 'dashboard/manage_slideshow.html', context)


@staff_member_required
def manage_deals(request):
    """Manage deals and promotions"""
    from products.models import Deal, Product
    from django.utils import timezone
    
    deals = Deal.objects.all().order_by('-created_at')
    
    # Update deal statuses based on dates
    now = timezone.now()
    for deal in deals:
        if deal.status == 'scheduled' and deal.start_date <= now:
            deal.status = 'active'
            deal.save()
        elif deal.status == 'active' and deal.end_date < now:
            deal.status = 'expired'
            deal.save()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        deals = deals.filter(status=status_filter)
    
    # Get all products for the modal
    products = Product.objects.filter(is_active=True).order_by('name')
    
    context = {
        'deals': deals,
        'products': products,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/manage_deals_modal.html', context)


@staff_member_required
def add_deal(request):
    """Add a new deal via AJAX"""
    from products.models import Deal, Product
    from django.utils import timezone
    import json
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            deal_type = request.POST.get('deal_type')
            discount_percentage = request.POST.get('discount_percentage')
            discount_amount = request.POST.get('discount_amount')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            is_featured = request.POST.get('is_featured') == 'on'
            badge_text = request.POST.get('badge_text', '')
            max_uses = request.POST.get('max_uses')
            product_ids = request.POST.getlist('products')
            
            if title and deal_type and start_date and end_date and product_ids:
                deal = Deal.objects.create(
                    title=title,
                    description=description,
                    deal_type=deal_type,
                    discount_percentage=discount_percentage if discount_percentage else None,
                    discount_amount=discount_amount if discount_amount else None,
                    start_date=start_date,
                    end_date=end_date,
                    is_featured=is_featured,
                    badge_text=badge_text,
                    max_uses=max_uses if max_uses else None,
                    status='draft',
                    created_by=request.user
                )
                
                if 'banner_image' in request.FILES:
                    deal.banner_image = request.FILES['banner_image']
                    deal.save()
                
                # Add products to deal
                deal.products.set(Product.objects.filter(id__in=product_ids))
                
                return JsonResponse({'success': True, 'message': f'Deal "{title}" created successfully!'})
            else:
                return JsonResponse({'success': False, 'error': 'Please fill in all required fields.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@staff_member_required
def edit_deal(request, deal_id):
    """Edit an existing deal via AJAX"""
    from products.models import Deal, Product
    import json
    
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Deal not found'})
    
    if request.method == 'POST':
        try:
            deal.title = request.POST.get('title', deal.title)
            deal.description = request.POST.get('description', '')
            deal.deal_type = request.POST.get('deal_type', deal.deal_type)
            deal.discount_percentage = request.POST.get('discount_percentage') or None
            deal.discount_amount = request.POST.get('discount_amount') or None
            deal.start_date = request.POST.get('start_date', deal.start_date)
            deal.end_date = request.POST.get('end_date', deal.end_date)
            deal.is_featured = request.POST.get('is_featured') == 'on'
            deal.badge_text = request.POST.get('badge_text', '')
            deal.max_uses = request.POST.get('max_uses') or None
            deal.status = request.POST.get('status', deal.status)
            
            if 'banner_image' in request.FILES:
                deal.banner_image = request.FILES['banner_image']
            
            product_ids = request.POST.getlist('products')
            if product_ids:
                deal.products.set(Product.objects.filter(id__in=product_ids))
            
            deal.save()
            return JsonResponse({'success': True, 'message': f'Deal "{deal.title}" updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@staff_member_required
def get_deal(request, deal_id):
    """Get deal data for AJAX editing"""
    from products.models import Deal
    import json
    
    try:
        deal = Deal.objects.get(id=deal_id)
        
        data = {
            'id': deal.id,
            'title': deal.title,
            'description': deal.description,
            'deal_type': deal.deal_type,
            'discount_percentage': str(deal.discount_percentage) if deal.discount_percentage else '',
            'discount_amount': str(deal.discount_amount) if deal.discount_amount else '',
            'start_date': deal.start_date.strftime('%Y-%m-%d') if deal.start_date else '',
            'end_date': deal.end_date.strftime('%Y-%m-%d') if deal.end_date else '',
            'badge_text': deal.badge_text or '',
            'max_uses': deal.max_uses if deal.max_uses else '',
            'is_featured': deal.is_featured,
            'status': deal.status,
            'banner_image': deal.banner_image.url if deal.banner_image else '',
            'product_ids': list(deal.products.values_list('id', flat=True))
        }
        
        return JsonResponse(data)
    except Deal.DoesNotExist:
        return JsonResponse({'error': 'Deal not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def delete_deal(request, deal_id):
    """Delete a deal"""
    from products.models import Deal
    
    if request.method == 'POST':
        deal = get_object_or_404(Deal, id=deal_id)
        title = deal.title
        deal.delete()
        messages.success(request, f'Deal "{title}" deleted successfully!')
    
    return redirect('dashboard:manage_deals')


@staff_member_required
def toggle_deal_status(request, deal_id):
    """Toggle deal active/draft status"""
    from products.models import Deal
    
    if request.method == 'POST':
        deal = get_object_or_404(Deal, id=deal_id)
        
        if deal.status == 'active':
            deal.status = 'draft'
            status_text = 'deactivated'
        elif deal.status == 'draft':
            deal.status = 'active'
            status_text = 'activated'
        else:
            messages.error(request, 'Can only toggle between active and draft status.')
            return redirect('dashboard:manage_deals')
        
        deal.save()
        messages.success(request, f'Deal "{deal.title}" {status_text} successfully!')
    
    
    return redirect('dashboard:manage_deals')


@staff_member_required
def apply_deal(request, deal_id):
    """Apply deal discounts to products"""
    from products.models import Deal
    
    if request.method == 'POST':
        deal = get_object_or_404(Deal, id=deal_id)
        
        try:
            deal.apply_to_products()
            messages.success(request, f'Deal "{deal.title}" applied to {deal.products.count()} products successfully!')
        except Exception as e:
            messages.error(request, f'Error applying deal: {str(e)}')
    
    return redirect('dashboard:manage_deals')


# =============== ADMIN NOTIFICATION API ===============

@staff_member_required
def all_notifications(request):
    """View all notifications page"""
    from accounts.models import Notification
    
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    context = {
        'notifications': notifications,
        'page_title': 'All Notifications'
    }
    return render(request, 'dashboard/notifications.html', context)


@staff_member_required
def notifications_json(request):
    """Get admin notifications as JSON"""
    from accounts.models import Notification
    from django.utils.timesince import timesince
    
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:20]
    
    notification_list = []
    for notif in notifications:
        notification_list.append({
            'id': notif.id,
            'type': notif.notification_type,
            'title': notif.title,
            'message': notif.message,
            'link': notif.link or '#',
            'is_read': notif.is_read,
            'time': notif.created_at.isoformat(),
        })
    
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({
        'success': True,
        'notifications': notification_list,
        'unread_count': unread_count
    })


@staff_member_required
def mark_notification_read(request):
    """Mark a notification as read"""
    from accounts.models import Notification
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_id = data.get('notification_id')
            
            notification = Notification.objects.get(
                id=notification_id,
                user=request.user
            )
            notification.is_read = True
            notification.save()
            
            unread_count = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()
            
            return JsonResponse({
                'success': True,
                'unread_count': unread_count
            })
        except Notification.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Notification not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@staff_member_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    from accounts.models import Notification
    
    if request.method == 'POST':
        try:
            Notification.objects.filter(
                user=request.user,
                is_read=False
            ).update(is_read=True)
            
            return JsonResponse({
                'success': True,
                'message': 'All notifications marked as read'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
