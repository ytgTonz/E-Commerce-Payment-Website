from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'seller']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_id', 'customer__username', 'customer__email']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_id', 'customer', 'status')
        }),
        ('Payment', {
            'fields': ('total_amount', 'payment_method', 'payment_reference', 'paid_at')
        }),
        ('Delivery', {
            'fields': ('delivery_address', 'delivery_phone', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'product_price', 'seller']
    list_filter = ['seller', 'created_at']
    search_fields = ['product_name', 'order__order_id']
