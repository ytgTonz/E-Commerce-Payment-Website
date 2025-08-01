from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    """Form for checkout process"""
    
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_phone', 'notes']
        widgets = {
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your complete delivery address',
                'rows': 4,
                'required': True
            }),
            'delivery_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '+234 xxx xxxx xxx',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Any special delivery instructions (optional)',
                'rows': 3
            }),
        }
        labels = {
            'delivery_address': 'Delivery Address',
            'delivery_phone': 'Phone Number',
            'notes': 'Special Instructions'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_address'].required = True
        self.fields['delivery_phone'].required = True
        self.fields['notes'].required = False

class ShippingAddressForm(forms.Form):
    """Standalone shipping address form"""
    
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Full Name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Email Address'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '+234 xxx xxxx xxx'
        })
    )
    
    address_line_1 = forms.CharField(
        max_length=200,
        label='Street Address',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Street address, house number'
        })
    )
    
    address_line_2 = forms.CharField(
        max_length=200,
        label='Apartment/Suite',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Apartment, suite, unit (optional)'
        })
    )
    
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'City'
        })
    )
    
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'State'
        })
    )
    
    postal_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Postal Code (optional)'
        })
    )
    
    def get_formatted_address(self):
        """Get formatted address string"""
        address_parts = [
            self.cleaned_data.get('address_line_1', ''),
            self.cleaned_data.get('address_line_2', ''),
            self.cleaned_data.get('city', ''),
            self.cleaned_data.get('state', ''),
            self.cleaned_data.get('postal_code', ''),
        ]
        return ', '.join(filter(None, address_parts))