from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('order/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.order_history, name='order_history'),
    path('webhook/paystack/', views.paystack_webhook, name='paystack_webhook'),
]