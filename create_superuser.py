#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from accounts.models import User

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        user_type='seller'  # Make admin a seller so they can add products
    )
    print("SUCCESS: Superuser 'admin' created successfully!")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Email: admin@example.com")
else:
    print("WARNING: Superuser 'admin' already exists")