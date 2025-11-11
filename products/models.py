from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})


class Product(models.Model):
    """Product model"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    reviews_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0
    
    @property
    def has_active_deal(self):
        """Check if product has an active deal"""
        from django.utils import timezone
        now = timezone.now()
        return self.deals.filter(
            status='active',
            start_date__lte=now,
            end_date__gte=now
        ).exists()
    
    @property
    def active_deal(self):
        """Get the first active deal for this product"""
        from django.utils import timezone
        now = timezone.now()
        return self.deals.filter(
            status='active',
            start_date__lte=now,
            end_date__gte=now
        ).first()
    
    @property
    def discounted_price(self):
        """Get price after applying active deal discount"""
        deal = self.active_deal
        if deal:
            if deal.deal_type == 'percentage' and deal.discount_percentage:
                discount = float(self.price) * (float(deal.discount_percentage) / 100)
                return float(self.price) - discount
            elif deal.deal_type == 'fixed' and deal.discount_amount:
                return max(0, float(self.price) - float(deal.discount_amount))
        return float(self.price)
    
    @property
    def original_price(self):
        """Get original price (for showing strikethrough)"""
        if self.has_active_deal:
            return float(self.price)
        elif self.old_price and self.old_price > self.price:
            return float(self.old_price)
        return None
    
    @property
    def final_price(self):
        """Get final price to display (with deal applied if exists)"""
        return self.discounted_price
    
    @property
    def savings_amount(self):
        """Calculate savings amount"""
        original = self.original_price
        if original:
            return original - self.discounted_price
        return 0
    
    @property
    def savings_percentage(self):
        """Calculate savings percentage"""
        original = self.original_price
        if original and original > 0:
            return int(((original - self.discounted_price) / original) * 100)
        return 0
    
    def update_rating(self):
        """Update product rating and review count"""
        from django.db.models import Avg, Count
        stats = self.reviews.aggregate(avg_rating=Avg('rating'), total_reviews=Count('id'))
        self.rating = stats['avg_rating'] or 0.00
        self.reviews_count = stats['total_reviews'] or 0
        self.save(update_fields=['rating', 'reviews_count'])
    
    def get_all_images(self):
        """Get all images including the main image"""
        images = []
        # Add main image first
        if self.image:
            images.append({
                'url': self.image.url,
                'is_primary': True
            })
        # Add additional images
        for img in self.images.all():
            images.append({
                'url': img.image.url,
                'is_primary': img.is_primary
            })
        return images
    
    def get_primary_image(self):
        """Get the primary image (either main image or marked primary from gallery)"""
        primary_gallery = self.images.filter(is_primary=True).first()
        if primary_gallery:
            return primary_gallery.image.url
        return self.image.url if self.image else None


class Slide(models.Model):
    """Homepage carousel slides"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='slides/')
    link = models.URLField(blank=True)
    button_text = models.CharField(max_length=50, default='Shop Now')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """Multiple images for a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['order', '-is_primary']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images for this product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductReview(models.Model):
    """Product reviews and ratings"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ['-created_at']
        unique_together = [['product', 'user', 'order']]  # One review per product per order
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.product.name} ({self.rating} stars)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update product's average rating and review count
        self.product.update_rating()


class Deal(models.Model):
    """Deal/Promotion model for managing special offers"""
    DEAL_TYPE_CHOICES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount Discount'),
        ('bogo', 'Buy One Get One'),
        ('bundle', 'Bundle Deal'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('scheduled', 'Scheduled'),
        ('expired', 'Expired'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES, default='percentage')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, 
                                             help_text="Percentage discount (0-100)")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         help_text="Fixed amount discount")
    
    # Products included in the deal
    products = models.ManyToManyField(Product, related_name='deals', blank=True)
    
    # Deal validity
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Deal settings
    is_featured = models.BooleanField(default=False, help_text="Show in featured deals section")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    max_uses = models.PositiveIntegerField(blank=True, null=True, help_text="Maximum number of times this deal can be used")
    current_uses = models.PositiveIntegerField(default=0)
    
    # Deal display
    banner_image = models.ImageField(upload_to='deals/', blank=True, null=True)
    badge_text = models.CharField(max_length=50, blank=True, help_text="Custom badge text (e.g., 'HOT DEAL')")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_deals')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def is_active(self):
        """Check if deal is currently active"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date and
            (self.max_uses is None or self.current_uses < self.max_uses)
        )
    
    def get_discount_display(self):
        """Get formatted discount string"""
        if self.deal_type == 'percentage' and self.discount_percentage:
            return f"{self.discount_percentage}% OFF"
        elif self.deal_type == 'fixed' and self.discount_amount:
            return f"₱{self.discount_amount} OFF"
        elif self.deal_type == 'bogo':
            return "Buy 1 Get 1 FREE"
        elif self.deal_type == 'bundle':
            return "Bundle Deal"
        return "Special Offer"
    
    def apply_to_products(self):
        """Apply this deal to all associated products"""
        for product in self.products.all():
            if self.deal_type == 'percentage' and self.discount_percentage:
                discount = float(product.price) * (float(self.discount_percentage) / 100)
                product.old_price = product.price
                product.price = product.price - discount
            elif self.deal_type == 'fixed' and self.discount_amount:
                product.old_price = product.price
                product.price = max(0, product.price - self.discount_amount)
            
            product.on_sale = True
            product.save()

