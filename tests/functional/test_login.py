#!/usr/bin/env python
"""
Test script to verify login functionality
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def test_login_functionality():
    """Test the login functionality with admin user"""
    print("Testing login functionality...")
    
    # Create a test client
    client = Client()
    
    # Test GET request to login page
    print("1. Testing login page access...")
    response = client.get('/accounts/login/')
    print(f"   Login page status: {response.status_code}")
    print(f"   Content type: {response.get('content-type', 'Not set')}")
    
    if response.status_code == 200:
        print("   SUCCESS: Login page loads successfully")
    else:
        print(f"   ERROR: Login page failed to load: {response.status_code}")
        return
    
    # Test POST request with admin credentials
    print("2. Testing login with admin credentials...")
    login_data = {
        'login': 'admin',
        'password': 'admin123',
    }
    
    response = client.post('/accounts/login/', login_data)
    print(f"   Login POST status: {response.status_code}")
    
    if response.status_code == 302:
        print("   SUCCESS: Login successful (redirected)")
        print(f"   Redirect location: {response.get('Location', 'Not set')}")
    else:
        print(f"   ERROR: Login failed: {response.status_code}")
        if hasattr(response, 'context') and response.context:
            form = response.context.get('form')
            if form and form.errors:
                print(f"   Form errors: {form.errors}")
    
    # Test accessing authenticated page
    print("3. Testing authenticated access...")
    response = client.get('/user/profile/')
    print(f"   Profile page status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ Can access authenticated pages after login")
    elif response.status_code == 302:
        print("   → Redirected (may need login)")
    else:
        print(f"   ✗ Cannot access authenticated pages: {response.status_code}")
    
    print("\nLogin functionality test completed!")

if __name__ == '__main__':
    test_login_functionality()