from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    """
    A class to manage the shopping cart using Django sessions.
    """
    
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        # Get the current cart from the session, or create a new one if it doesn't exist
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        
        # If product not in cart, add it
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        # Update quantity: override or increment
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        """
        Save the cart in the session.
        """
        self.session.modified = True
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        
        # Get product objects
        products = Product.objects.filter(id__in=product_ids)
        
        # Create a copy of the cart to avoid modifying the original
        cart = self.cart.copy()
        
        # Add product objects to the cart items
        for product in products:
            cart[str(product.id)]['product'] = product
        
        # Calculate item total prices
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """
        Clear the cart.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
