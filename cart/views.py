from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product

@login_required
def cart_detail(request):
    """Display user's shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart via AJAX"""
    product = get_object_or_404(Product, id=product_id, status='active')
    
    if not product.is_available:
        return JsonResponse({
            'success': False,
            'message': 'This product is not available.'
        })
    
    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get quantity from request
    quantity = int(request.POST.get('quantity', 1))
    
    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        # Item already in cart, increase quantity
        new_quantity = cart_item.quantity + quantity
        if new_quantity <= product.stock_quantity:
            cart_item.quantity = new_quantity
            cart_item.save()
            message = f'Updated {product.name} quantity in your cart.'
        else:
            message = f'Cannot add more {product.name}. Stock limit reached.'
            return JsonResponse({
                'success': False,
                'message': message
            })
    else:
        message = f'Added {product.name} to your cart.'
    
    return JsonResponse({
        'success': True,
        'message': message,
        'cart_count': cart.total_items,
        'cart_total': str(cart.total_price)
    })

@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, f'Removed {cart_item.product.name} from your cart.')
    elif quantity <= cart_item.product.stock_quantity:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Updated {cart_item.product.name} quantity.')
    else:
        messages.error(request, f'Cannot set quantity to {quantity}. Only {cart_item.product.stock_quantity} available.')
    
    return redirect('cart:detail')

@login_required
@require_POST
def remove_cart_item(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    if request.headers.get('Content-Type') == 'application/json':
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'message': f'Removed {product_name} from your cart.',
            'cart_count': cart.total_items,
            'cart_total': str(cart.total_price)
        })
    
    messages.success(request, f'Removed {product_name} from your cart.')
    return redirect('cart:detail')

@login_required
def clear_cart(request):
    """Clear all items from cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.clear()
    messages.success(request, 'Your cart has been cleared.')
    return redirect('cart:detail')

@login_required
def cart_count(request):
    """Return cart count for AJAX requests"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return JsonResponse({
        'cart_count': cart.total_items,
        'cart_total': str(cart.total_price)
    })
