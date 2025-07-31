#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from accounts.models import User
from products.models import Product, Category
from decimal import Decimal

def create_sample_data():
    print("Creating sample data for Django Marketplace...")
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    
    # Create categories
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and gadgets', 'slug': 'electronics'},
        {'name': 'Clothing', 'description': 'Fashion and apparel', 'slug': 'clothing'},
        {'name': 'Books', 'description': 'Books and educational materials', 'slug': 'books'},
        {'name': 'Home & Garden', 'description': 'Home improvement and gardening', 'slug': 'home-garden'},
        {'name': 'Sports', 'description': 'Sports and fitness equipment', 'slug': 'sports'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create sample products
    products_data = [
        {
            'name': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.',
            'price': Decimal('89.99'),
            'category': 'Electronics',
            'stock_quantity': 25,
        },
        {
            'name': 'Smartphone Case',
            'description': 'Durable protective case for smartphones. Drop-proof and scratch-resistant with easy access to all ports.',
            'price': Decimal('19.99'),
            'category': 'Electronics',
            'stock_quantity': 50,
        },
        {
            'name': 'Cotton T-Shirt',
            'description': 'Comfortable 100% cotton t-shirt available in multiple colors and sizes. Machine washable and pre-shrunk.',
            'price': Decimal('24.99'),
            'category': 'Clothing',
            'stock_quantity': 30,
        },
        {
            'name': 'Programming Book: Python for Beginners',
            'description': 'Comprehensive guide to learning Python programming from scratch. Includes practical examples and exercises.',
            'price': Decimal('39.99'),
            'category': 'Books',
            'stock_quantity': 15,
        },
        {
            'name': 'Garden Tool Set',
            'description': 'Complete 5-piece garden tool set including spade, rake, pruning shears, and more. Perfect for gardening enthusiasts.',
            'price': Decimal('49.99'),
            'category': 'Home & Garden',
            'stock_quantity': 20,
        },
        {
            'name': 'Yoga Mat',
            'description': 'Premium non-slip yoga mat with excellent cushioning. Eco-friendly and easy to clean. Perfect for yoga and fitness.',
            'price': Decimal('34.99'),
            'category': 'Sports',
            'stock_quantity': 40,
        },
        {
            'name': 'Laptop Stand',
            'description': 'Adjustable aluminum laptop stand for better ergonomics. Compatible with all laptop sizes and foldable for portability.',
            'price': Decimal('59.99'),
            'category': 'Electronics',
            'stock_quantity': 12,
        },
        {
            'name': 'Coffee Mug Set',
            'description': 'Set of 4 ceramic coffee mugs with unique designs. Microwave and dishwasher safe. Perfect for coffee lovers.',
            'price': Decimal('29.99'),
            'category': 'Home & Garden',
            'stock_quantity': 18,
        },
    ]
    
    for product_data in products_data:
        category = Category.objects.get(name=product_data['category'])
        product_data['category'] = category
        product_data['seller'] = admin_user
        
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"Created product: {product.name}")
    
    print(f"\nSample data creation complete!")
    print(f"Categories: {Category.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print("\nYou can now visit the homepage to see the products!")

if __name__ == '__main__':
    create_sample_data()