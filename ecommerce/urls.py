"""
URL configuration for ecommerce project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('products/', views.products_page, name='products'),
    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('orders/', views.orders_page, name='orders'),
    path('order-success/', views.order_success_page, name='order_success'),
    path('product-details/', views.product_details_page, name='product_details'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/<int:product_id>/', views.api_product_detail, name='api_product_detail'),
    path('api/cart/', views.api_cart_list, name='api_cart_list'),
    path('api/cart/add/', views.api_cart_add, name='api_cart_add'),
    path('api/cart/remove/', views.api_cart_remove, name='api_cart_remove'),
    path('api/checkout/', views.api_checkout, name='api_checkout'),
    path('api/orders/list/', views.api_orders_list, name='api_orders_list'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
