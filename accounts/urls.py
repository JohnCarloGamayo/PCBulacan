from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('account/', views.account_view, name='account'),
    path('ajax/cancel-order/', views.cancel_order, name='cancel_order'),
    path('ajax/mark-received/', views.mark_received, name='mark_received'),
    path('ajax/get-order-address/', views.get_order_address, name='get_order_address'),
    path('ajax/submit-ratings/', views.submit_product_ratings, name='submit_ratings'),
    path('ajax/get-order-items-for-rating/', views.get_order_items_for_rating, name='get_order_items_for_rating'),
    
    # Forgot password endpoints
    path('ajax/send-reset-code/', views.send_reset_code, name='send_reset_code'),
    path('ajax/verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('ajax/reset-password/', views.reset_password, name='reset_password'),
]
