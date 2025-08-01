from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import User
from products.models import Product, Category


class CustomSignupForm(SignupForm):
    """
    Custom signup form that extends allauth's SignupForm
    to include user_type selection
    """
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        initial='buyer',
        widget=forms.RadioSelect,
        help_text='Choose your account type'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes and attributes to form fields
        self.fields['username'].widget.attrs.update({
            'class': 'w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Choose a username',
            'autocomplete': 'username'
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password'
        })

    def save(self, request):
        # Save the user with the default allauth process
        user = super().save(request)
        
        # Set the user_type from the form
        user.user_type = self.cleaned_data['user_type']
        user.save()
        
        return user


class CustomLoginForm(LoginForm):
    """
    Custom login form that extends allauth's LoginForm
    with better styling and field attributes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes and attributes to form fields
        self.fields['login'].widget.attrs.update({
            'class': 'w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Username or Email',
            'autocomplete': 'username'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        })
        
        if 'remember' in self.fields:
            self.fields['remember'].widget.attrs.update({
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'user_type']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Address',
                'rows': 3
            }),
            'user_type': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True


class ProductForm(forms.ModelForm):
    """
    Form for sellers to add/edit products
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock_quantity', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Describe your product...',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '0',
                'min': '0'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required except image
        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.required = True
        
        # Add help text
        self.fields['price'].help_text = 'Price in South African Rand (ZAR)'
        self.fields['stock_quantity'].help_text = 'Number of items available'
        self.fields['image'].help_text = 'Upload a product image (optional)'