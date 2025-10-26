from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='list'),
    path('product/<slug:slug>/', views.product_detail_view, name='detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('api/product/<int:product_id>/', views.product_detail_api, name='product_detail_api'),
]
