from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Adds user_type field to distinguish between buyers and sellers
    """
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='buyer',
        help_text='Type of user - buyer or seller'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text='Phone number for contact'
    )
    
    address = models.TextField(
        blank=True,
        help_text='User address for delivery'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_seller(self):
        """Check if user is a seller"""
        return self.user_type == 'seller'
    
    def is_buyer(self):
        """Check if user is a buyer"""
        return self.user_type == 'buyer'
