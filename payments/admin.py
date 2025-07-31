from django.contrib import admin
from .models import Payment, PaymentHistory

class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0
    readonly_fields = ['status', 'notes', 'created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'order', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'currency', 'created_at']
    search_fields = ['reference', 'gateway_reference', 'order__order_id', 'customer_email']
    list_editable = ['status']
    inlines = [PaymentHistoryInline]
    readonly_fields = ['payment_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('payment_id', 'reference', 'order', 'status')
        }),
        ('Amount', {
            'fields': ('amount', 'currency', 'gateway_fee')
        }),
        ('Gateway', {
            'fields': ('payment_method', 'gateway_reference', 'gateway_response')
        }),
        ('Customer', {
            'fields': ('customer_email', 'customer_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at')
        }),
    )

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['payment', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['payment__reference', 'notes']
