from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, Category, Slide
from dashboard.models import SlideshowImage


@login_required
def home_view(request):
    """Homepage with all products and carousel"""
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


@login_required
def product_list_view(request):
    """Display all products with filtering and pagination"""
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


@login_required
def product_detail_view(request, slug):
    """Display single product details"""
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


@login_required
def category_view(request, slug):
    """Display products by category"""
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


@login_required
def product_detail_api(request, product_id):
    """API endpoint for product details (for modal)"""
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
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
