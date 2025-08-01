from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from decimal import Decimal
import json
import uuid
import requests
import hmac
import hashlib

from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm, ShippingAddressForm
from payments.models import Payment


@login_required
def checkout(request):
    """Checkout page with order summary and payment"""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')
    
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')
    
    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST)
        
        if shipping_form.is_valid():
            # Create the order
            order = Order.objects.create(
                customer=request.user,
                total_amount=cart.total_price,
                delivery_address=shipping_form.get_formatted_address(),
                delivery_phone=shipping_form.cleaned_data['phone'],
                payment_method='paystack'
            )
            
            # Create order items from cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.price,
                    quantity=cart_item.quantity,
                    seller=cart_item.product.seller
                )
                
                # Reduce product stock
                cart_item.product.reduce_stock(cart_item.quantity)
            
            # Create payment record
            payment_reference = f"MP_{order.order_id.hex[:8].upper()}_{int(timezone.now().timestamp())}"
            payment = Payment.objects.create(
                reference=payment_reference,
                order=order,
                amount=order.total_amount,
                customer_email=request.user.email,
                customer_phone=shipping_form.cleaned_data['phone']
            )
            
            # Initialize Paystack payment
            paystack_data = {
                'email': request.user.email,
                'amount': int(order.total_amount * 100),  # Paystack expects amount in kobo
                'reference': payment_reference,
                'callback_url': request.build_absolute_uri(reverse('orders:checkout_success')),
                'metadata': {
                    'order_id': str(order.order_id),
                    'customer_id': str(request.user.id),
                    'customer_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
                }
            }
            
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            
            try:
                response = requests.post(
                    'https://api.paystack.co/transaction/initialize',
                    json=paystack_data,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    paystack_response = response.json()
                    if paystack_response['status']:
                        # Store the authorization URL in session
                        request.session['order_id'] = str(order.order_id)
                        request.session['payment_reference'] = payment_reference
                        
                        # Clear the cart
                        cart.items.all().delete()
                        
                        # Redirect to Paystack
                        return redirect(paystack_response['data']['authorization_url'])
                    else:
                        messages.error(request, 'Payment initialization failed. Please try again.')
                        order.delete()  # Clean up failed order
                else:
                    messages.error(request, 'Payment service is currently unavailable. Please try again.')
                    order.delete()  # Clean up failed order
                    
            except requests.RequestException:
                messages.error(request, 'Payment service is currently unavailable. Please try again.')
                order.delete()  # Clean up failed order
    else:
        # Pre-fill form with user data
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone', ''),
        }
        shipping_form = ShippingAddressForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'shipping_form': shipping_form,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def checkout_success(request):
    """Handle successful payment callback"""
    reference = request.GET.get('reference')
    
    if not reference:
        messages.error(request, 'Invalid payment reference.')
        return redirect('cart:detail')
    
    try:
        payment = Payment.objects.get(reference=reference)
        order = payment.order
        
        # Verify payment with Paystack
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        }
        
        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            paystack_data = response.json()
            
            if paystack_data['status'] and paystack_data['data']['status'] == 'success':
                # Payment successful
                payment.status = 'successful'
                payment.gateway_response = paystack_data['data']
                payment.gateway_reference = paystack_data['data'].get('reference', '')
                payment.paid_at = timezone.now()
                payment.save()
                
                # Update order
                order.status = 'paid'
                order.payment_reference = reference
                order.paid_at = timezone.now()
                order.save()
                
                messages.success(request, f'Payment successful! Your order #{order.order_id} has been confirmed.')
                return render(request, 'orders/checkout_success.html', {'order': order, 'payment': payment})
            else:
                # Payment failed
                payment.status = 'failed'
                payment.gateway_response = paystack_data['data']
                payment.save()
                
                order.status = 'cancelled'
                order.save()
                
                messages.error(request, 'Payment was not successful. Please try again.')
                return redirect('orders:checkout_cancel')
        else:
            messages.error(request, 'Unable to verify payment. Please contact support.')
            return redirect('orders:checkout_cancel')
            
    except Payment.DoesNotExist:
        messages.error(request, 'Payment record not found.')
        return redirect('cart:detail')
    except requests.RequestException:
        messages.error(request, 'Unable to verify payment. Please contact support.')
        return redirect('orders:checkout_cancel')


@login_required
def checkout_cancel(request):
    """Handle cancelled payment"""
    return render(request, 'orders/checkout_cancel.html')


@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, order_id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history(request):
    """View user's order history"""
    orders = Order.objects.filter(customer=request.user).prefetch_related('items', 'payments')
    return render(request, 'orders/order_history.html', {'orders': orders})


@csrf_exempt
@require_POST
def paystack_webhook(request):
    """Handle Paystack webhook notifications"""
    # Verify webhook signature
    signature = request.headers.get('X-Paystack-Signature', '')
    
    computed_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
        request.body,
        hashlib.sha512
    ).hexdigest()
    
    if not hmac.compare_digest(signature, computed_signature):
        return HttpResponse('Invalid signature', status=400)
    
    try:
        payload = json.loads(request.body)
        event = payload.get('event')
        data = payload.get('data', {})
        
        if event == 'charge.success':
            reference = data.get('reference')
            if reference:
                try:
                    payment = Payment.objects.get(reference=reference)
                    if payment.status != 'successful':
                        payment.status = 'successful'
                        payment.gateway_response = data
                        payment.paid_at = timezone.now()
                        payment.save()
                        
                        # Update order
                        order = payment.order
                        order.status = 'paid'
                        order.paid_at = timezone.now()
                        order.save()
                        
                except Payment.DoesNotExist:
                    pass  # Payment not found, ignore
        
        return HttpResponse('OK', status=200)
        
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON', status=400)
    except Exception as e:
        return HttpResponse('Error processing webhook', status=500)
