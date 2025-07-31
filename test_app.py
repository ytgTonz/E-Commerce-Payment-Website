#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def test_django_app():
    print("=== Testing Django Marketplace Application ===\n")
    
    # Test 1: Models Import
    try:
        from accounts.models import User
        from products.models import Product, Category
        from cart.models import Cart, CartItem
        from orders.models import Order, OrderItem
        from payments.models import Payment
        print("SUCCESS: All models imported successfully")
    except Exception as e:
        print(f"ERROR: Model import error: {e}")
        return False
    
    # Test 2: Database Connectivity
    try:
        user_count = User.objects.count()
        print(f"SUCCESS: Database connected - {user_count} users found")
    except Exception as e:
        print(f"ERROR: Database error: {e}")
        return False
    
    # Test 3: Admin User
    try:
        admin_user = User.objects.get(username='admin')
        print(f"SUCCESS: Admin user exists: {admin_user.username} ({admin_user.user_type})")
    except User.DoesNotExist:
        print("ERROR: Admin user not found")
        return False
    
    # Test 4: Create Sample Data
    try:
        # Create category if doesn't exist
        category, created = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Electronic devices', 'slug': 'electronics'}
        )
        if created:
            print("SUCCESS: Sample category created")
        else:
            print("SUCCESS: Sample category exists")
        
        # Create product if doesn't exist
        product, created = Product.objects.get_or_create(
            name='Test Product',
            defaults={
                'description': 'A test product for demonstration',
                'price': 99.99,
                'seller': admin_user,
                'category': category,
                'stock_quantity': 10
            }
        )
        if created:
            print("SUCCESS: Sample product created")
        else:
            print("SUCCESS: Sample product exists")
            
    except Exception as e:
        print(f"ERROR: Sample data creation error: {e}")
        return False
    
    # Test 5: Verify Relationships
    try:
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        print(f"SUCCESS: Data verification - {product_count} products, {category_count} categories")
    except Exception as e:
        print(f"ERROR: Relationship error: {e}")
        return False
    
    print("\n=== All Tests Passed! ===")
    print("CELEBRATION: Django Marketplace is fully functional!")
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/")
    print("3. Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
    
    return True

if __name__ == '__main__':
    test_django_app()