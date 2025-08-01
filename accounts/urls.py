from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # User profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Seller dashboard URLs
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
]