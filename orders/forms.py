from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    """
    Form for creating a new order during checkout.
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 
                 'address', 'city', 'province', 'postal_code',
                 'payment_method', 'note']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
