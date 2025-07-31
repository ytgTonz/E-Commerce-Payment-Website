from django.db import models
from django.conf import settings
from django.urls import reverse
from PIL import Image
import os

def product_image_path(instance, filename):
    """Generate file path for product images"""
    return f'products/{instance.seller.username}/{filename}'

class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Product model based on Flask app structure"""
    name = models.CharField(max_length=200, help_text='Product name')
    description = models.TextField(blank=True, help_text='Product description')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Product price in your local currency'
    )
    image = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True,
        help_text='Product image'
    )
    
    # Foreign Keys
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        help_text='Product seller'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    # Product status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('sold', 'Sold'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    # Additional fields for better e-commerce functionality
    stock_quantity = models.PositiveIntegerField(default=1)
    featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if it exists
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    @property
    def is_available(self):
        """Check if product is available for purchase"""
        return self.status == 'active' and self.stock_quantity > 0
    
    def reduce_stock(self, quantity=1):
        """Reduce stock quantity"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            if self.stock_quantity == 0:
                self.status = 'sold'
            self.save()
            return True
        return False

class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images'
    )
    image = models.ImageField(upload_to=product_image_path)
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
