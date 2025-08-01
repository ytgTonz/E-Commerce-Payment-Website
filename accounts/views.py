from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from .forms import UserProfileForm, ProductForm
from .models import User
from products.models import Product
from orders.models import Order, OrderItem


@login_required
def profile_view(request):
    """Display user profile"""
    return render(request, 'account/profile.html', {
        'user': request.user
    })


@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'account/profile_edit.html', {
        'form': form
    })


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'account/change_password.html', {
        'form': form
    })


def seller_required(view_func):
    """Decorator to ensure only sellers can access seller views"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        if not request.user.is_seller():
            messages.error(request, 'You need to be a seller to access this page.')
            return redirect('accounts:profile')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@seller_required
def seller_dashboard(request):
    """Seller dashboard homepage with analytics"""
    seller = request.user
    
    # Get seller's products
    products = Product.objects.filter(seller=seller)
    total_products = products.count()
    active_products = products.filter(is_active=True).count()
    
    # Get seller's orders through their products
    order_items = OrderItem.objects.filter(product__seller=seller)
    
    # Calculate analytics
    total_sales = order_items.aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    total_orders = order_items.values('order').distinct().count()
    
    # Get recent orders
    recent_orders = order_items.select_related('order', 'product').order_by('-order__created_at')[:5]
    
    # Low stock products (less than 5 items)
    low_stock_products = products.filter(stock_quantity__lt=5, is_active=True)
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    
    return render(request, 'seller/dashboard.html', context)


@login_required
@seller_required
def seller_products(request):
    """Seller products management page"""
    seller = request.user
    products_list = Product.objects.filter(seller=seller).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'search_query': search_query,
    }
    
    return render(request, 'seller/products.html', context)


@login_required
@seller_required
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" has been added successfully!')
            return redirect('accounts:seller_products')
    else:
        form = ProductForm()
    
    return render(request, 'seller/add_product.html', {
        'form': form
    })


@login_required
@seller_required
def edit_product(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully!')
            return redirect('accounts:seller_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'seller/edit_product.html', {
        'form': form,
        'product': product
    })


@login_required
@seller_required
def delete_product(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('accounts:seller_products')
    
    return render(request, 'seller/delete_product.html', {
        'product': product
    })


@login_required
@seller_required
def seller_orders(request):
    """Seller orders management"""
    seller = request.user
    
    # Get orders that contain seller's products
    order_items = OrderItem.objects.filter(
        product__seller=seller
    ).select_related('order', 'product').order_by('-order__created_at')
    
    # Group by order
    orders_dict = {}
    for item in order_items:
        order_id = item.order.id
        if order_id not in orders_dict:
            orders_dict[order_id] = {
                'order': item.order,
                'items': [],
                'total': 0
            }
        orders_dict[order_id]['items'].append(item)
        orders_dict[order_id]['total'] += item.total_price
    
    orders_list = list(orders_dict.values())
    
    # Pagination
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    return render(request, 'seller/orders.html', {
        'orders': orders
    })
