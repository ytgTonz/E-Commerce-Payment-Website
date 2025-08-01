#!/usr/bin/env python
"""
Test the fallback redirect from /accounts/profile/ to /user/profile/
"""
import os
import django
from django.test import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def test_profile_redirect():
    """Test that /accounts/profile/ redirects to /user/profile/"""
    print("Testing profile URL redirect fallback...")
    
    client = Client()
    
    # Login first
    login_data = {
        'login': 'admin',
        'password': 'admin123',
    }
    client.post('/accounts/login/', login_data)
    
    print("\n=== Testing Fallback Redirect ===")
    
    # Test accessing the old profile URL
    response = client.get('/accounts/profile/', follow=True)
    
    print(f"Final response status: {response.status_code}")
    print(f"Final URL: {response.wsgi_request.path}")
    
    # Check redirect chain
    if hasattr(response, 'redirect_chain'):
        print("Redirect chain:")
        for redirect_url, status_code in response.redirect_chain:
            print(f"  -> {redirect_url} (status: {status_code})")
    
    if response.wsgi_request.path == '/user/profile/':
        print("SUCCESS: /accounts/profile/ correctly redirects to /user/profile/")
    else:
        print(f"ERROR: Unexpected final URL: {response.wsgi_request.path}")
    
    print("\nProfile redirect test completed!")

if __name__ == '__main__':
    test_profile_redirect()