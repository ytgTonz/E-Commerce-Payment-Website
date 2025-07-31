from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('product/<int:pk>/', views.product_detail, name='detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
]