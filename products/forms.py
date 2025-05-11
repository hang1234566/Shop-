from django import forms
from .models import Review, Product

class ReviewForm(forms.ModelForm):
    """Form for product reviews."""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ProductSearchForm(forms.Form):
    """Form for product search and filtering."""
    search = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tìm kiếm sản phẩm...'})
    )
    min_price = forms.DecimalField(
        required=False, 
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá tối thiểu'})
    )
    max_price = forms.DecimalField(
        required=False, 
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá tối đa'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError("Giá tối thiểu không thể cao hơn giá tối đa.")
        
        return cleaned_data
