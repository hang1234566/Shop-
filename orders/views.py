from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart

@login_required
def order_create(request):
    """
    View to handle order creation (checkout process).
    """
    cart = Cart(request)
    
    # Check if cart is empty
    if not cart.cart:
        messages.warning(request, 'Giỏ hàng của bạn đang trống, vui lòng thêm sản phẩm trước khi thanh toán.')
        return redirect('cart:cart_detail')
    
    # Pre-fill form with user profile data if available
    initial_data = {}
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': profile.phone_number,
            'address': profile.address,
            'city': profile.city,
            'province': profile.province,
            'postal_code': profile.postal_code,
        }
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            # Create order items from the cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            
            # Store order in session for order confirmation
            request.session['order_id'] = order.id
            
            return redirect('orders:order_confirmation')
    else:
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

@login_required
def order_confirmation(request):
    """
    View to display order confirmation after successful checkout.
    """
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        # Clear the order from session to prevent multiple refreshes
        if 'order_id' in request.session:
            del request.session['order_id']
        return render(request, 'orders/order_confirmation.html', {'order': order})
    return redirect('home')

@login_required
def order_history(request):
    """
    View to display user's order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """
    View to display details of a specific order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
