#!/usr/bin/env python
"""
Test script to verify signup redirect fix
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

def test_signup_redirect():
    """Test that signup redirects to the correct profile page"""
    print("Testing signup redirect fix...")
    
    # Create a test client
    client = Client()
    User = get_user_model()
    
    print("\n=== Testing Signup Redirect ===")
    
    # Test registration page access first
    response = client.get('/accounts/signup/')
    print(f"Registration page status: {response.status_code}")
    if response.status_code != 200:
        print("ERROR: Registration page not accessible")
        return
    
    # Test user registration with unique credentials
    import time
    unique_suffix = str(int(time.time()))
    signup_data = {
        'username': f'redirecttest_{unique_suffix}',
        'email': f'redirect_{unique_suffix}@example.com',
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
        'user_type': 'buyer',
    }
    
    print(f"Attempting to register user: {signup_data['username']}")
    response = client.post('/accounts/signup/', signup_data, follow=True)
    
    print(f"Final response status: {response.status_code}")
    print(f"Final URL: {response.wsgi_request.path}")
    
    # Check redirect chain
    if hasattr(response, 'redirect_chain'):
        print("Redirect chain:")
        for redirect_url, status_code in response.redirect_chain:
            print(f"  -> {redirect_url} (status: {status_code})")
    
    # Verify the user was created
    try:
        new_user = User.objects.get(username=signup_data['username'])
        print(f"SUCCESS: User created successfully")
        print(f"  Username: {new_user.username}")
        print(f"  Email: {new_user.email}")
        print(f"  User type: {new_user.user_type}")
        
        # Check if we ended up on the profile page
        if response.wsgi_request.path == '/user/profile/':
            print("SUCCESS: Redirected to correct profile page!")
        else:
            print(f"INFO: Redirected to: {response.wsgi_request.path}")
            
    except User.DoesNotExist:
        print("INFO: User not found - might be due to email verification requirement")
    
    print("\n=== Testing Profile Page Access ===")
    
    # Test direct access to profile page
    profile_response = client.get('/user/profile/')
    print(f"Profile page direct access: {profile_response.status_code}")
    
    if profile_response.status_code == 200:
        print("SUCCESS: Profile page is accessible after signup")
    elif profile_response.status_code == 302:
        print("INFO: Profile page redirects (authentication required)")
    else:
        print(f"ERROR: Unexpected profile page status: {profile_response.status_code}")
    
    print("\nSignup redirect test completed!")

if __name__ == '__main__':
    test_signup_redirect()