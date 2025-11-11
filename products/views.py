from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Slide, Deal
from dashboard.models import SlideshowImage
from orders.models import Order, OrderItem, DeliveryFee
import re


def home_view(request):
    """Homepage with all products and carousel - accessible to everyone"""
    # Get main slideshow images and static banners
    main_slides = SlideshowImage.objects.filter(is_active=True, slide_type='main').order_by('order')
    banner_slides = SlideshowImage.objects.filter(is_active=True, slide_type='banner').order_by('order')[:2]
    
    all_products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)[:6]
    context = {
        'main_slides': main_slides,
        'banner_slides': banner_slides,
        'all_products': all_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)


def deals_view(request):
    """Deals page with featured deals and discounted products - accessible to everyone"""
    # Get main slideshow images only (no banners)
    main_slides = SlideshowImage.objects.filter(is_active=True, slide_type='main').order_by('order')
    
    # Get active deals
    now = timezone.now()
    active_deals = Deal.objects.filter(
        status='active',
        start_date__lte=now,
        end_date__gte=now
    ).select_related().prefetch_related('products')
    
    # Get all products from active deals
    deal_product_ids = []
    for deal in active_deals:
        deal_product_ids.extend(deal.products.values_list('id', flat=True))
    
    # Get products on sale or in active deals
    deal_products = Product.objects.filter(
        Q(is_active=True) & (Q(on_sale=True) | Q(id__in=deal_product_ids))
    ).distinct()
    
    # Get featured deals (products)
    featured_deals = Product.objects.filter(is_active=True, is_featured=True)[:8]
    
    # Get categories for filtering
    categories = Category.objects.filter(is_active=True)
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        deal_products = deal_products.filter(category__id=category_filter)
    
    # Sort options
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        deal_products = deal_products.order_by('price')
    elif sort_by == 'price_high':
        deal_products = deal_products.order_by('-price')
    elif sort_by == 'discount':
        deal_products = deal_products.order_by('-discount_percentage')
    else:
        deal_products = deal_products.order_by('-created_at')
    
    context = {
        'main_slides': main_slides,
        'deal_products': deal_products,
        'featured_deals': featured_deals,
        'active_deals': active_deals,
        'categories': categories,
        'selected_category': category_filter,
        'sort_by': sort_by,
    }
    return render(request, 'products/deals.html', context)


def support_view(request):
    """Customer support page"""
    return render(request, 'support.html')


@csrf_exempt
def chat_api(request):
    """AI Chat API endpoint - Enhanced with 74+ Q&A scenarios"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'response': '👋 Hi! Kumusta! I\'m your AI assistant. Ask me about:\n'
                            '📦 Orders • 💰 Prices • 🚚 Shipping • 💳 Payment • 🛍️ Products'
            })
        
        # Use enhanced AI response system
        from ai_training_data import get_ai_response
        response_text = get_ai_response(message)
        
        return JsonResponse({
            'response': response_text
        })
        
    except Exception as e:
        import traceback
        print(f"Chat API Error: {e}")
        traceback.print_exc()
        return JsonResponse({
            'response': 'Sorry, may problema sa system. Please try again or contact support at (044) 123-4567.'
        })


def parse_and_respond(message, user):
    """Parse user message and generate response based on database queries"""
    
    # ORDER QUERY - Check order status
    if any(keyword in message for keyword in ['order', 'orders', 'tracking', 'kamusta', 'status']):
        # Extract order number if mentioned
        order_match = re.search(r'(ord[-\s]?\w+|\b\w{10}\b)', message, re.IGNORECASE)
        
        if order_match:
            order_number = order_match.group(1).upper().replace(' ', '-')
            if not order_number.startswith('ORD-'):
                order_number = f'ORD-{order_number}'
            
            try:
                order = Order.objects.select_related('user').prefetch_related('items__product').get(order_number=order_number)
                
                # Check if user owns this order (if authenticated)
                if user and user.is_authenticated and order.user != user:
                    return {
                        'response': f'Sorry, hindi kita mahanap ang order na {order_number} under your account.'
                    }
                
                items_list = ', '.join([f"{item.quantity}x {item.product.name}" for item in order.items.all()[:3]])
                if order.items.count() > 3:
                    items_list += f' and {order.items.count() - 3} more items'
                
                status_tagalog = {
                    'pending': 'Pending (waiting for confirmation)',
                    'processing': 'Processing (preparing your order)',
                    'shipped': 'Shipped (on the way)',
                    'delivered': 'Delivered',
                    'received': 'Received',
                    'cancelled': 'Cancelled'
                }
                
                return {
                    'response': f'Nakita ko ang order mo **{order.order_number}**!\n\n'
                                f'📦 **Status:** {status_tagalog.get(order.status, order.status)}\n'
                                f'💰 **Total:** ₱{order.total:,.2f}\n'
                                f'📅 **Ordered:** {order.created_at.strftime("%B %d, %Y")}\n'
                                f'🛍️ **Items:** {items_list}\n'
                                f'🚚 **Shipping:** {order.city}, {order.state}\n\n'
                                f'Need more help? Just ask!',
                    'data': {
                        'order_number': order.order_number,
                        'status': order.status,
                        'total': float(order.total),
                        'items_count': order.items.count()
                    }
                }
            except Order.DoesNotExist:
                return {
                    'response': f'Sorry, hindi ko mahanap ang order **{order_number}**. Please check the order number or log in to view your orders.'
                }
        
        # If no specific order mentioned, show user's recent orders
        if user and user.is_authenticated:
            recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:3]
            if recent_orders.exists():
                orders_info = []
                for order in recent_orders:
                    status_tagalog = {
                        'pending': 'Pending',
                        'processing': 'Processing',
                        'shipped': 'Shipped',
                        'delivered': 'Delivered',
                        'received': 'Received',
                        'cancelled': 'Cancelled'
                    }
                    orders_info.append(f"• **{order.order_number}** - {status_tagalog.get(order.status, order.status)} (₱{order.total:,.2f})")
                
                return {
                    'response': f'Here are your recent orders:\n\n' + '\n'.join(orders_info) + 
                                '\n\nTo get details about a specific order, just tell me the order number!'
                }
            else:
                return {
                    'response': 'You don\'t have any orders yet. Browse our products and make your first purchase!'
                }
        else:
            return {
                'response': 'Please provide an order number (e.g., ORD-ABC1234567) or log in to view your orders.'
            }
    
    # PRODUCT RECOMMENDATION - Recommend products
    elif any(keyword in message for keyword in ['product', 'recommend', 'best', 'maganda', 'suggest', 'bili', 'category']):
        # Extract category if mentioned
        categories = Category.objects.filter(is_active=True)
        matched_category = None
        
        for category in categories:
            if category.name.lower() in message:
                matched_category = category
                break
        
        if matched_category:
            top_products = Product.objects.filter(
                category=matched_category,
                is_active=True
            ).order_by('-rating', '-created_at')[:3]
            
            if top_products.exists():
                products_list = []
                for i, product in enumerate(top_products, 1):
                    price_info = f"₱{product.price:,.2f}"
                    if product.discount_percentage and product.discount_percentage > 0:
                        price_info += f" **({product.discount_percentage}% OFF!)**"
                    products_list.append(f"{i}. **{product.name}** - {price_info}")
                
                return {
                    'response': f'Here are my top {matched_category.name} recommendations:\n\n' +
                                '\n'.join(products_list) +
                                f'\n\nAll products are authentic and brand new! Visit our shop to see more {matched_category.name}.',
                    'data': {
                        'category': matched_category.name,
                        'products': [{'name': p.name, 'price': float(p.price)} for p in top_products]
                    }
                }
            else:
                return {
                    'response': f'Sorry, wala kaming available na {matched_category.name} products right now. Try another category!'
                }
        else:
            # No specific category, show featured products
            featured = Product.objects.filter(is_active=True, is_featured=True).order_by('-rating')[:3]
            if featured.exists():
                products_list = []
                for i, product in enumerate(featured, 1):
                    products_list.append(f"{i}. **{product.name}** - ₱{product.price:,.2f}")
                
                available_categories = ', '.join([cat.name for cat in categories[:5]])
                return {
                    'response': 'Here are our featured products:\n\n' +
                                '\n'.join(products_list) +
                                f'\n\nWe have products in: {available_categories}. Just tell me which category you\'re interested in!'
                }
            else:
                return {
                    'response': 'We have many products available! What category are you interested in? (Processors, Graphics Cards, etc.)'
                }
    
    # SHIPPING QUERY - Calculate shipping fees
    elif any(keyword in message for keyword in ['shipping', 'delivery', 'ship', 'deliver', 'paano', 'magkano', 'fee', 'cost', 'tagal']):
        # Extract city and state from message
        delivery_fees = DeliveryFee.objects.filter(is_available=True)
        matched_location = None
        best_match_score = 0
        
        # Try to match city and state combinations
        for fee in delivery_fees:
            score = 0
            city_lower = fee.city.lower()
            state_lower = fee.state.lower()
            
            # Check if both city and state are in message (best match)
            if city_lower in message and state_lower in message:
                score = 3
            # Check if city is in message
            elif city_lower in message:
                score = 2
            # Check if state is in message
            elif state_lower in message:
                score = 1
            
            if score > best_match_score:
                best_match_score = score
                matched_location = fee
        
        if matched_location:
            return {
                'response': f'📍 **Shipping to {matched_location.city}, {matched_location.state}:**\n\n'
                            f'💵 **Shipping Fee:** ₱{matched_location.fee_amount:,.2f}\n'
                            f'⏱️ **Estimated Delivery:** {matched_location.estimated_days}\n'
                            f'🎁 **Free Shipping:** Orders over ₱{matched_location.min_order_free_delivery:,.2f}\n\n'
                            f'Your order will arrive within {matched_location.estimated_days}!',
                'data': {
                    'city': matched_location.city,
                    'state': matched_location.state,
                    'fee_amount': float(matched_location.fee_amount),
                    'estimated_days': matched_location.estimated_days
                }
            }
        else:
            # Show general shipping info
            sample_fees = delivery_fees[:5]
            if sample_fees.exists():
                fees_list = '\n'.join([f"• **{fee.city}, {fee.state}:** ₱{fee.fee_amount:,.2f} ({fee.estimated_days})" for fee in sample_fees])
                return {
                    'response': f'🚚 **Our Shipping Rates:**\n\n{fees_list}\n\n'
                                f'Tell me your city/province and I\'ll give you the exact shipping cost!\n'
                                f'⏱️ Delivery: 3-5 days Metro Manila, 5-7 days provincial'
                }
            else:
                return {
                    'response': '🚚 Standard shipping: ₱100-300 depending on location.\n'
                                '⏱️ Delivery time: 3-5 business days Metro Manila, 5-7 days provincial.\n\n'
                                'Tell me your city for exact shipping cost!'
                }
    
    # PAYMENT QUERY - Show payment methods
    elif any(keyword in message for keyword in ['payment', 'pay', 'bayad', 'method', 'gcash', 'cod', 'bank']):
        return {
            'response': '💳 **Available Payment Methods:**\n\n'
                        '1. **Bank Transfer** 🏦\n'
                        '   - BDO, BPI, Metrobank, UnionBank\n'
                        '   - Upload payment screenshot after ordering\n\n'
                        '2. **GCash** 📱\n'
                        '   - Upload screenshot after payment\n\n'
                        '3. **PayMaya** 💰\n'
                        '   - Upload screenshot after payment\n\n'
                        '4. **Cash on Delivery (COD)** 💵\n'
                        '   - Available for select locations only\n'
                        '   - Pay when you receive your order\n\n'
                        'All payments are secure and verified!',
            'data': {
                'methods': ['Bank Transfer', 'GCash', 'PayMaya', 'Cash on Delivery']
            }
        }
    
    # WARRANTY/RETURN QUERY
    elif any(keyword in message for keyword in ['warranty', 'return', 'refund', 'guarantee', 'ibalik']):
        return {
            'response': '✅ **Warranty & Returns:**\n\n'
                        '📋 **Return Policy:**\n'
                        '• 30-day return window\n'
                        '• Products must be unused and in original packaging\n'
                        '• Some items (software, opened electronics) not eligible\n\n'
                        '🛡️ **Warranty:**\n'
                        '• All products 100% authentic and brand new\n'
                        '• Manufacturer warranty included (1-3 years)\n'
                        '• Extended warranty available for select items\n\n'
                        'Need help with a return? Contact us with your order number!'
        }
    
    # CONTACT/SUPPORT QUERY
    elif any(keyword in message for keyword in ['contact', 'support', 'help', 'tulong', 'email', 'phone']):
        return {
            'response': '📞 **Contact Us:**\n\n'
                        '📱 **Phone:** (044) 123-4567\n'
                        '📧 **Email:** support@pcbulacan.com\n'
                        '⏰ **Hours:** Mon-Sat, 9AM-6PM\n\n'
                        '💬 Or continue chatting with me! I can help you with:\n'
                        '• Order tracking\n'
                        '• Product recommendations\n'
                        '• Shipping information\n'
                        '• Payment methods\n'
                        '• And more!'
        }
    
    # GENERAL GREETING
    elif any(keyword in message for keyword in ['hi', 'hello', 'kumusta', 'hey', 'help', 'tulong']):
        return {
            'response': '👋 Hello! Welcome to PCBulacan!\n\n'
                        'I\'m your AI assistant. I can help you with:\n\n'
                        '📦 **Order Tracking** - Check your order status\n'
                        '🛍️ **Product Recommendations** - Find the best products\n'
                        '🚚 **Shipping Info** - Get delivery time and fees\n'
                        '💳 **Payment Methods** - See available payment options\n'
                        '🛡️ **Warranty & Returns** - Learn about our policies\n\n'
                        'Just ask me anything! For example:\n'
                        '• "Kamusta yung order ko ORD-123?"\n'
                        '• "Ano best graphics card?"\n'
                        '• "Magkano shipping sa Manila?"'
        }
    
    # DEFAULT RESPONSE
    else:
        return {
            'response': 'I\'m not sure I understand. 🤔\n\n'
                        'I can help you with:\n'
                        '• **Orders** - Track your order status\n'
                        '• **Products** - Get recommendations\n'
                        '• **Shipping** - Check delivery fees and time\n'
                        '• **Payment** - View payment methods\n'
                        '• **Returns** - Learn about our return policy\n\n'
                        'Try asking me something like:\n'
                        '"Kamusta order ko?" or "Ano best processor?"'
        }


def product_list_view(request):
    """Display all products with filtering and pagination - accessible to everyone"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Filter by category (support multiple categories)
    category_filter = request.GET.getlist('category')
    selected_categories = []
    if category_filter:
        products = products.filter(category__id__in=category_filter)
        selected_categories = list(map(int, category_filter))
    
    # Price range filter
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=float(price_min))
    if price_max:
        products = products.filter(price__lte=float(price_max))
    
    # In stock filter
    in_stock = request.GET.get('in_stock')
    if in_stock == '1':
        products = products.filter(stock__gt=0)
    
    # On sale filter
    on_sale = request.GET.get('on_sale')
    if on_sale == '1':
        products = products.filter(on_sale=True)
    
    # Search functionality
    search_query = request.GET.get('search') or request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:  # default
        products = products.order_by('-is_featured', '-created_at')
    
    # No pagination - show all filtered products
    total_products = products.count()
    
    context = {
        'products': products,
        'all_products': products,  # For JavaScript filtering
        'categories': categories,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_products': total_products,
        'selected_categories': selected_categories,
        'price_min': price_min or '',
        'price_max': price_max or '',
        'in_stock': in_stock,
        'on_sale': on_sale,
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """Display single product details - accessible to everyone"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def category_view(request, slug):
    """Display products by category - accessible to everyone"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products_page,
    }
    return render(request, 'products/category.html', context)


def search_suggestions(request):
    """API endpoint for live search suggestions"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 1:
        return JsonResponse([], safe=False)
    
    # Search products by name
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_active=True
    ).values('name')[:10]
    
    # Extract unique product names
    suggestions = [product['name'] for product in products]
    
    return JsonResponse(suggestions, safe=False)


def product_detail_api(request, product_id):
    """API endpoint for product details (for modal) - accessible to everyone"""
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Get reviews for this product
        reviews = []
        for review in product.reviews.all().order_by('-created_at'):
            reviews.append({
                'id': review.id,
                'user_name': review.user.get_full_name(),
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%B %d, %Y'),
            })
        
        # Get all product images
        images = []
        if product.image:
            images.append({
                'url': product.image.url,
                'is_primary': True
            })
        for img in product.images.all():
            images.append({
                'url': img.image.url,
                'is_primary': img.is_primary
            })
        
        # Get deal information
        active_deal = product.active_deal
        
        data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'old_price': float(product.old_price) if product.old_price else None,
            'on_sale': product.on_sale,
            'stock': product.stock,
            'category': product.category.name,
            'image': product.image.url if product.image else None,
            'images': images,
            'created_at': product.created_at.isoformat(),
            'rating': float(product.rating),
            'reviews_count': product.reviews_count,
            'reviews': reviews,
            # Deal information
            'has_active_deal': product.has_active_deal,
            'final_price': float(product.final_price),
            'original_price': float(product.original_price),
            'savings_amount': float(product.savings_amount),
            'savings_percentage': int(product.savings_percentage),
            'active_deal_name': active_deal.title if active_deal else None,
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
