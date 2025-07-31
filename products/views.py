from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category
from cart.models import Cart, CartItem

def product_list(request):
    """Homepage with product listings"""
    products = Product.objects.filter(status='active').select_related('seller', 'category')
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Category filtering
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    """Product detail page"""
    product = get_object_or_404(Product, pk=pk, status='active')
    related_products = Product.objects.filter(
        category=product.category,
        status='active'
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_to_cart(request, pk):
    """Add product to cart - redirect to cart add URL"""
    return redirect('cart:add', product_id=pk)
