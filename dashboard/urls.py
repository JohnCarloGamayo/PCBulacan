from django.urls import path
from . import views, ajax_views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    
    # User management
    path('users/', views.manage_users, name='manage_users'),
    path('users/view/<int:user_id>/', views.view_user, name='view_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    
    # Product management
    path('products/', views.manage_products, name='manage_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/delete-image/<int:image_id>/', views.delete_product_image, name='delete_product_image'),
    
    # Slideshow management
    path('slideshow/', views.manage_slideshow, name='manage_slideshow'),
    
    # Deals management
    path('deals/', views.manage_deals, name='manage_deals'),
    path('deals/add/', views.add_deal, name='add_deal'),
    path('deals/get/<int:deal_id>/', views.get_deal, name='get_deal'),
    path('deals/edit/<int:deal_id>/', views.edit_deal, name='edit_deal'),
    path('deals/delete/<int:deal_id>/', views.delete_deal, name='delete_deal'),
    path('deals/toggle/<int:deal_id>/', views.toggle_deal_status, name='toggle_deal_status'),
    path('deals/apply/<int:deal_id>/', views.apply_deal, name='apply_deal'),

    # Inventory management
    path('inventory/', views.inventory_management, name='inventory_management'),
    path('inventory/print-report/', views.print_inventory_report, name='print_inventory_report'),
    path('inventory/export-pdf/', views.export_inventory_pdf, name='export_inventory_pdf'),
    
    # Order management
    path('orders/', views.manage_orders, name='manage_orders'),
    path('orders/<str:order_number>/details/', views.order_details, name='order_details'),
    path('orders/<str:order_number>/update-status/', views.update_order_status, name='update_order_status'),
    path('orders/export-pdf/', views.export_orders_pdf, name='export_orders_pdf'),
    
    # Category management
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    
    # Delivery fees management
    path('delivery-fees/', views.manage_delivery_fees, name='manage_delivery_fees'),
    path('delivery-fees/add/', views.add_delivery_fee, name='add_delivery_fee'),
    path('delivery-fees/edit/<int:fee_id>/', views.edit_delivery_fee, name='edit_delivery_fee'),
    path('delivery-fees/delete/<int:fee_id>/', views.delete_delivery_fee, name='delete_delivery_fee'),
    path('delivery-fees/toggle/<int:fee_id>/', views.toggle_delivery_fee_status, name='toggle_delivery_fee_status'),
    
    # Sales analytics
    path('sales-analytics/', views.sales_analytics, name='sales_analytics'),
    path('sales-analytics/export-pdf/', views.export_sales_analytics_pdf, name='export_sales_analytics_pdf'),
    
    # Payment history
    path('payment-history/', views.payment_history, name='payment_history'),
    path('payment-history/<str:order_number>/details/', views.payment_details_json, name='payment_details_json'),
    path('payment-history/export-pdf/', views.export_payment_history_pdf, name='export_payment_history_pdf'),
    
    # User management exports
    path('users/export-pdf/', views.export_users_pdf, name='export_users_pdf'),
    
    # Admin account
    path('admin-account/', views.admin_account, name='admin_account'),
    
    # Admin notifications
    path('notifications/', views.all_notifications, name='all_notifications'),
    path('notifications/json/', views.notifications_json, name='notifications_json'),
    path('notifications/mark_read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark_all_read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # AJAX endpoints for dashboard
    path('ajax/metrics/', ajax_views.dashboard_metrics, name='ajax_metrics'),
    path('ajax/sales-overview/', ajax_views.dashboard_sales_overview, name='ajax_sales_overview'),
    path('ajax/sales-by-category/', ajax_views.dashboard_sales_by_category, name='ajax_sales_category'),
    path('ajax/recent-orders/', ajax_views.dashboard_recent_orders, name='ajax_recent_orders'),
    path('ajax/top-products/', ajax_views.dashboard_top_products, name='ajax_top_products'),
    path('ajax/products-check/', ajax_views.dashboard_products_check, name='ajax_products_check'),
    
    # Dashboard data endpoints
    path('api/sales-data/', views.dashboard_sales_data, name='dashboard_sales_data'),
    path('api/recent-orders/', views.dashboard_recent_orders, name='dashboard_recent_orders'),
    path('api/top-products/', views.dashboard_top_products, name='dashboard_top_products'),
]