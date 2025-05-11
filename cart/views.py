from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    """
    View to add a product to the cart or update its quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Add product to cart
    cart.add(product=product, quantity=quantity, override_quantity=False)
    
    messages.success(request, f'Đã thêm "{product.name}" vào giỏ hàng.')
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    """
    View to update the quantity of a product in the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Update product quantity
    cart.add(product=product, quantity=quantity, override_quantity=True)
    
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    """
    View to remove a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Remove product from cart
    cart.remove(product)
    
    messages.info(request, f'Đã xóa "{product.name}" khỏi giỏ hàng.')
    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    View to display the cart contents.
    """
    cart = Cart(request)
    
    # Enable updating quantities directly in the cart
    for item in cart:
        item['update_quantity_form'] = {'quantity': item['quantity']}
    
    return render(request, 'cart/cart.html', {'cart': cart})
