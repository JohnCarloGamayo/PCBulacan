from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation_view, name='order_confirmation'),
    path('orders/', views.order_list_view, name='order_list'),
    path('order/<str:order_number>/', views.order_detail_view, name='order_detail'),
]
