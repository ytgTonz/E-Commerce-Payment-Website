from django.db import models
from django.conf import settings
from orders.models import Order
import uuid

class Payment(models.Model):
    """Payment tracking model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('paystack', 'Paystack'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash on Delivery'),
    ]
    
    # Payment identification
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(max_length=100, unique=True, help_text='Payment gateway reference')
    
    # Related order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='paystack')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Gateway specific data
    gateway_response = models.JSONField(null=True, blank=True, help_text='Full gateway response')
    gateway_reference = models.CharField(max_length=100, blank=True)
    gateway_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Customer info (from gateway)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['order', '-created_at']),
        ]
    
    def __str__(self):
        return f"Payment {self.reference} - {self.amount} {self.currency}"
    
    @property
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'successful'
    
    @property
    def is_pending(self):
        """Check if payment is pending"""
        return self.status == 'pending'
    
    def mark_as_successful(self, gateway_data=None):
        """Mark payment as successful"""
        self.status = 'successful'
        if gateway_data:
            self.gateway_response = gateway_data
        self.save()
    
    def mark_as_failed(self, gateway_data=None):
        """Mark payment as failed"""
        self.status = 'failed'
        if gateway_data:
            self.gateway_response = gateway_data
        self.save()

class PaymentHistory(models.Model):
    """Track payment status changes"""
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='history'
    )
    
    status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Payment Histories'
    
    def __str__(self):
        return f"{self.payment.reference} - {self.status}"
