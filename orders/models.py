from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    """
    Model for storing order information
    """
    STATUS_CHOICES = (
        ('pending', 'Đang xử lý'),
        ('processing', 'Đang chuẩn bị'),
        ('shipped', 'Đã gửi hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    )
    
    PAYMENT_CHOICES = (
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('e_wallet', 'Ví điện tử'),
        ('credit_card', 'Thẻ tín dụng'),
    )
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    note = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        """Calculate the total cost of the order."""
        return sum(item.get_cost() for item in self.items.all())
    
    def get_status_display_label(self):
        """Get the display label for the current status with appropriate CSS class."""
        status_classes = {
            'pending': 'secondary',
            'processing': 'primary',
            'shipped': 'info',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        
        return {
            'label': dict(self.STATUS_CHOICES)[self.status],
            'class': status_classes.get(self.status, 'secondary')
        }

class OrderItem(models.Model):
    """
    Model for storing order items
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity}x {self.product.name} in Order {self.order.id}'
    
    def get_cost(self):
        """Calculate the cost of this order item."""
        return self.price * self.quantity
