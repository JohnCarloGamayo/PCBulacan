from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F
from products.models import Product, Category
from orders.models import Order, OrderItem
from accounts.models import User
from datetime import datetime, timedelta
from django.utils import timezone

@staff_member_required
def dashboard_metrics(request):
    """Return dashboard metrics as JSON"""
    try:
        # Get total sales (completed orders only)
        total_sales = Order.objects.filter(
            status__in=['shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get total orders (exclude cancelled)
        total_orders = Order.objects.exclude(status='cancelled').count()
        
        # Get pending orders
        pending_orders = Order.objects.filter(status='pending').count()
        
        # Get low stock items (stock <= 10)
        low_stock_items = Product.objects.filter(stock__lte=10).count()
        
        return JsonResponse({
            'success': True,
            'data': {
                'totalSales': float(total_sales),
                'totalOrders': total_orders,
                'pendingOrders': pending_orders,
                'lowStockItems': low_stock_items
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@staff_member_required
def dashboard_sales_overview(request):
    """Return sales overview data for chart"""
    try:
        today = timezone.now().date()
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Get current week data
        current_week_start = today - timedelta(days=today.weekday())
        current_week_data = []
        
        for i in range(7):
            day = current_week_start + timedelta(days=i)
            sales = Order.objects.filter(
                created_at__date=day,
                status__in=['shipped', 'delivered']
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            current_week_data.append(float(sales))
        
        # Get previous week data
        prev_week_start = current_week_start - timedelta(days=7)
        prev_week_data = []
        
        for i in range(7):
            day = prev_week_start + timedelta(days=i)
            sales = Order.objects.filter(
                created_at__date=day,
                status__in=['shipped', 'delivered']
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            prev_week_data.append(float(sales))
        
        return JsonResponse({
            'success': True,
            'data': {
                'labels': days_of_week,
                'currentWeek': current_week_data,
                'prevWeek': prev_week_data
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@staff_member_required
def dashboard_sales_by_category(request):
    """Return sales by category for pie chart"""
    try:
        # Get sales by category from order items
        category_sales = OrderItem.objects.filter(
            order__status__in=['shipped', 'delivered']
        ).values('product__category__name').annotate(
            total=Sum('total')
        ).order_by('-total')[:5]
        
        labels = []
        data = []
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
        
        for item in category_sales:
            labels.append(item['product__category__name'] or 'Uncategorized')
            data.append(float(item['total']))
        
        # If no data, use sample data
        if not labels:
            labels = ['Processors', 'Graphics Cards', 'Motherboards', 'Memory', 'Storage']
            data = [30000, 25000, 20000, 15000, 10000]
        
        return JsonResponse({
            'success': True,
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': colors[:len(labels)]
                }]
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@staff_member_required
def dashboard_recent_orders(request):
    """Return recent orders"""
    try:
        orders = Order.objects.filter(
            status='pending'
        ).select_related('user').order_by('-created_at')[:5]
        
        data = []
        for order in orders:
            data.append({
                'id': order.id,
                'customer': order.user.get_full_name(),
                'date': order.created_at.strftime('%b %d, %Y %H:%M'),
                'amount': f"{order.total_amount:.2f}",
                'status': order.get_status_display()
            })
        
        return JsonResponse({
            'success': True,
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@staff_member_required
def dashboard_top_products(request):
    """Return top selling products"""
    try:
        # Get top products by quantity sold
        top_products = OrderItem.objects.filter(
            order__status__in=['shipped', 'delivered']
        ).values('product__name', 'product__category__name').annotate(
            quantity_sold=Sum('quantity'),
            revenue=Sum('total')
        ).order_by('-revenue')[:5]
        
        data = []
        for item in top_products:
            data.append({
                'product_name': item['product__name'],
                'category': item['product__category__name'] or 'Uncategorized',
                'quantity_sold': item['quantity_sold'],
                'revenue': f"{item['revenue']:.2f}"
            })
        
        # If no data, use sample data
        if not data:
            data = [
                {
                    'product_name': 'AMD Ryzen 9 5900X',
                    'category': 'Processors',
                    'quantity_sold': 25,
                    'revenue': '12500.00'
                },
                {
                    'product_name': 'NVIDIA RTX 3080',
                    'category': 'Graphics Cards',
                    'quantity_sold': 18,
                    'revenue': '14400.00'
                }
            ]
        
        return JsonResponse({
            'success': True,
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@staff_member_required
def dashboard_products_check(request):
    """Check for low stock products"""
    try:
        low_stock_threshold = 10
        low_stock_products = Product.objects.filter(
            stock__lte=low_stock_threshold
        ).select_related('category')[:10]
        
        products_list = []
        for product in low_stock_products:
            products_list.append({
                'id': product.id,
                'name': product.name,
                'category': product.category.name if product.category else 'Uncategorized',
                'stock': product.stock,
                'image': product.image.url if product.image else '/static/images/no-image.png'
            })
        
        return JsonResponse({
            'success': True,
            'data': {
                'totalProducts': Product.objects.count(),
                'lowStockItems': len(products_list),
                'lowStockThreshold': low_stock_threshold,
                'lowStockProducts': products_list
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
