#!/usr/bin/env python
"""
Test script for checkout and payment flow
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def test_checkout_flow():
    """Test the complete checkout flow"""
    print("Testing checkout and payment flow...")
    
    # Create a test client
    client = Client()
    User = get_user_model()
    
    # Login with admin user
    login_data = {
        'login': 'admin',
        'password': 'admin123',
    }
    login_response = client.post('/accounts/login/', login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code != 302:
        print("ERROR: Cannot login to test checkout")
        return
    
    print("\n=== Testing Checkout Page Access ===")
    
    # Test checkout page access (should redirect if cart is empty)
    checkout_response = client.get('/orders/checkout/')
    print(f"Checkout page status: {checkout_response.status_code}")
    
    if checkout_response.status_code == 302:
        print("INFO: Redirected - likely due to empty cart")
        
        # Let's add an item to cart first
        print("\n=== Adding Item to Cart ===")
        from products.models import Product
        from cart.models import Cart, CartItem
        
        # Get first available product
        product = Product.objects.filter(stock__gt=0).first()
        if product:
            print(f"Adding product: {product.name}")
            
            # Add item to cart via AJAX endpoint
            add_to_cart_data = {
                'product_id': product.id,
                'quantity': 1
            }
            add_response = client.post('/cart/add/', add_to_cart_data)
            print(f"Add to cart status: {add_response.status_code}")
            
            # Try checkout again
            checkout_response = client.get('/orders/checkout/')
            print(f"Checkout page status after adding item: {checkout_response.status_code}")
            
            if checkout_response.status_code == 200:
                print("SUCCESS: Checkout page loads with items in cart")
                
                # Test checkout form submission
                print("\n=== Testing Checkout Form ===")
                checkout_form_data = {
                    'full_name': 'Test User',
                    'email': 'test@example.com',
                    'phone': '+2341234567890',
                    'address_line_1': '123 Test Street',
                    'city': 'Lagos',
                    'state': 'Lagos State',
                }
                
                # Note: This will try to initialize payment with Paystack
                # In a real test environment, you'd mock the Paystack API
                checkout_submit_response = client.post('/orders/checkout/', checkout_form_data)
                print(f"Checkout form submission status: {checkout_submit_response.status_code}")
                
                if checkout_submit_response.status_code == 302:
                    print("INFO: Checkout redirected (likely to payment gateway or error page)")
                elif checkout_submit_response.status_code == 200:
                    print("INFO: Checkout form validation - check for errors in response")
                else:
                    print(f"UNEXPECTED: Checkout form status: {checkout_submit_response.status_code}")
            else:
                print(f"ERROR: Checkout page not accessible: {checkout_response.status_code}")
        else:
            print("ERROR: No products available to add to cart")
    elif checkout_response.status_code == 200:
        print("SUCCESS: Checkout page loads directly")
    else:
        print(f"ERROR: Unexpected checkout status: {checkout_response.status_code}")
    
    print("\n=== Testing Other Order URLs ===")
    
    # Test order history page
    history_response = client.get('/orders/my-orders/')
    print(f"Order history status: {history_response.status_code}")
    
    # Test checkout cancel page
    cancel_response = client.get('/orders/checkout/cancel/')
    print(f"Checkout cancel status: {cancel_response.status_code}")
    
    print("\nCheckout flow test completed!")
    print("\nNOTE: Full payment testing requires Paystack test keys and mock responses.")
    print("The checkout flow structure is ready for integration testing.")

if __name__ == '__main__':
    test_checkout_flow()