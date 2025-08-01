#!/usr/bin/env python
"""
Test script to verify login redirect issue
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def test_login_redirect():
    """Test that login redirects correctly"""
    print("Testing login redirect issue...")
    
    # Create a test client
    client = Client()
    User = get_user_model()
    
    print("\n=== Testing Login Redirect ===")
    
    # Test login page access first
    response = client.get('/accounts/login/')
    print(f"Login page status: {response.status_code}")
    if response.status_code != 200:
        print("ERROR: Login page not accessible")
        return
    
    # Test login with admin credentials
    login_data = {
        'login': 'admin',
        'password': 'admin123',
    }
    
    print("Attempting to login with admin credentials...")
    response = client.post('/accounts/login/', login_data, follow=True)
    
    print(f"Final response status: {response.status_code}")
    print(f"Final URL: {response.wsgi_request.path}")
    
    # Check redirect chain
    if hasattr(response, 'redirect_chain'):
        print("Redirect chain:")
        for redirect_url, status_code in response.redirect_chain:
            print(f"  -> {redirect_url} (status: {status_code})")
    else:
        print("No redirect chain found")
    
    # Check if we got a 404
    if response.status_code == 404:
        print("ERROR: Login resulted in 404 - redirect URL not found")
        print("This suggests the redirect URL doesn't exist")
    elif response.status_code == 200:
        print("SUCCESS: Login completed successfully")
        print(f"User is now on: {response.wsgi_request.path}")
    else:
        print(f"INFO: Login response status: {response.status_code}")
    
    print("\n=== Testing Homepage Access ===")
    
    # Test direct access to homepage
    homepage_response = client.get('/')
    print(f"Homepage direct access: {homepage_response.status_code}")
    
    if homepage_response.status_code == 200:
        print("SUCCESS: Homepage is accessible")
    else:
        print(f"ERROR: Homepage not accessible: {homepage_response.status_code}")
    
    print("\n=== Testing Profile Page Access After Login ===")
    
    # Test profile page access
    profile_response = client.get('/user/profile/')
    print(f"Profile page access: {profile_response.status_code}")
    
    if profile_response.status_code == 200:
        print("SUCCESS: Profile page is accessible after login")
    else:
        print(f"ERROR: Profile page not accessible: {profile_response.status_code}")
    
    print("\nLogin redirect test completed!")

if __name__ == '__main__':
    test_login_redirect()