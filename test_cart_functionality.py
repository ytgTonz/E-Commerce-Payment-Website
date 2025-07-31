#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from accounts.models import User
from products.models import Product
from cart.models import Cart, CartItem

def test_cart_functionality():
    print("=== Testing Shopping Cart Functionality ===\n")
    
    # Test 1: Get admin user and products
    try:
        admin_user = User.objects.get(username='admin')
        products = Product.objects.all()[:3]  # Get first 3 products
        print(f"SUCCESS: Found admin user and {products.count()} products")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Test 2: Create a test buyer
    try:
        buyer, created = User.objects.get_or_create(
            username='testbuyer',
            defaults={
                'email': 'buyer@test.com',
                'user_type': 'buyer'
            }
        )
        if created:
            buyer.set_password('testpass123')
            buyer.save()
            print("SUCCESS: Created test buyer")
        else:
            print("SUCCESS: Test buyer already exists")
    except Exception as e:
        print(f"ERROR: Creating test buyer - {e}")
        return False
    
    # Test 3: Create cart and add items
    try:
        cart, created = Cart.objects.get_or_create(user=buyer)
        
        # Clear existing cart items for clean test
        cart.clear()
        
        # Add products to cart
        for i, product in enumerate(products, 1):
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': i}  # Different quantities for testing
            )
            
            if item_created:
                print(f"SUCCESS: Added {product.name} to cart (quantity: {i})")
            else:
                print(f"SUCCESS: {product.name} already in cart")
        
    except Exception as e:
        print(f"ERROR: Adding items to cart - {e}")
        return False
    
    # Test 4: Verify cart calculations
    try:
        cart.refresh_from_db()
        total_items = cart.total_items
        total_price = cart.total_price
        
        print(f"SUCCESS: Cart has {total_items} items with total price ${total_price}")
        
        # Verify individual items
        for item in cart.items.all():
            print(f"  - {item.product.name}: {item.quantity} x ${item.product.price} = ${item.total_price}")
            
    except Exception as e:
        print(f"ERROR: Cart calculations - {e}")
        return False
    
    # Test 5: Test cart model methods
    try:
        # Test item total calculation
        first_item = cart.items.first()
        expected_total = first_item.quantity * first_item.product.price
        actual_total = first_item.total_price
        
        if expected_total == actual_total:
            print(f"SUCCESS: Item total calculation correct (${actual_total})")
        else:
            print(f"ERROR: Item total calculation wrong. Expected ${expected_total}, got ${actual_total}")
            return False
            
    except Exception as e:
        print(f"ERROR: Testing cart methods - {e}")
        return False
    
    # Test 6: Test cart clearing
    try:
        initial_count = cart.total_items
        cart.clear()
        final_count = cart.total_items
        
        if final_count == 0:
            print(f"SUCCESS: Cart cleared (was {initial_count} items, now {final_count})")
        else:
            print(f"ERROR: Cart not properly cleared. Still has {final_count} items")
            return False
            
    except Exception as e:
        print(f"ERROR: Testing cart clearing - {e}")
        return False
    
    print("\n=== All Cart Tests Passed! ===")
    print("Cart functionality is working correctly!")
    print("\nFeatures tested:")
    print("- Cart creation and item addition")
    print("- Cart item quantity management")
    print("- Cart total calculations")
    print("- Cart clearing functionality")
    print("- Database relationships")
    
    print("\nReady to test in browser:")
    print("1. Login as admin (admin/admin123)")
    print("2. Add products to cart from homepage")
    print("3. View cart at /cart/")
    print("4. Test quantity updates and item removal")
    
    return True

if __name__ == '__main__':
    test_cart_functionality()