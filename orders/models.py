from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('gcash', 'GCash'),
        ('paymaya', 'PayMaya'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    shipping_address = models.ForeignKey('accounts.UserAddress', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Shipping information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    
    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    notes = models.TextField(blank=True)
    deal_usage_counted = models.BooleanField(default=False, help_text="Track if deal usage has been counted for this order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Order {self.order_number}'
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f'ORD-{uuid.uuid4().hex[:10].upper()}'
        super().save(*args, **kwargs)
    
    @property
    def total_savings(self):
        """Calculate total savings from all items in this order"""
        return sum(item.savings_per_item * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # This stores the actual price paid (with discount if applicable)
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
    
    @property
    def total(self):
        return self.quantity * self.price
    
    @property
    def item_total(self):
        return self.quantity * self.price
    
    @property
    def had_discount(self):
        """Check if this item was purchased at a discount"""
        return float(self.price) < float(self.product.price)
    
    @property
    def original_price(self):
        """Original product price at time of display"""
        return float(self.product.price)
    
    @property
    def savings_per_item(self):
        """Amount saved per item"""
        if self.had_discount:
            return float(self.product.price) - float(self.price)
        return 0
    
    @property
    def savings_percentage(self):
        """Percentage discount"""
        if self.had_discount:
            return int(((float(self.product.price) - float(self.price)) / float(self.product.price)) * 100)
        return 0


class Cart(models.Model):
    """Shopping cart"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f'Cart for {self.user.email}'
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def unique_items_count(self):
        """Count unique products in cart (not total quantity)"""
        return self.items.count()
    
    @property
    def subtotal(self):
        """Subtotal with discounts applied"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_savings(self):
        """Total savings from all items"""
        return sum(item.total_savings for item in self.items.all())
    
    @property
    def original_subtotal(self):
        """Original subtotal before discounts"""
        return sum(item.quantity * item.original_unit_price for item in self.items.all())


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
    
    @property
    def unit_price(self):
        """Get the unit price (with deal discount if applicable)"""
        return self.product.final_price
    
    @property
    def original_unit_price(self):
        """Get original unit price before discount"""
        return self.product.original_price or self.product.price
    
    @property
    def total_price(self):
        """Total price for this cart item (with discount applied)"""
        return self.quantity * self.unit_price
    
    @property
    def total_savings(self):
        """Total savings for this item"""
        return self.quantity * self.product.savings_amount
    
    @property
    def has_discount(self):
        """Check if item has discount"""
        return self.product.has_active_deal or (self.product.old_price and self.product.old_price > self.product.price)


class DeliveryFee(models.Model):
    """Delivery fees based on location"""
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_free_delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Minimum order amount for free delivery")
    estimated_days = models.CharField(max_length=50, help_text="Estimated delivery time (e.g., '3-5 days')")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Delivery Fee'
        verbose_name_plural = 'Delivery Fees'
        unique_together = ('city', 'state')
        ordering = ['state', 'city']
    
    def __str__(self):
        return f"{self.city}, {self.state} - ₱{self.fee_amount}"
