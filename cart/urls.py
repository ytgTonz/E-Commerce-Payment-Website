from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_item'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_item'),
    path('clear/', views.clear_cart, name='clear'),
    path('count/', views.cart_count, name='count'),
]