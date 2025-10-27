from django.contrib import admin
from .models import Category, Product, Slide, ProductReview, ProductImage, Deal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'order', 'is_primary')
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'rating', 'reviews_count', 'is_active', 'is_featured', 'on_sale', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'is_new', 'on_sale', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_active', 'is_featured', 'on_sale')
    inlines = [ProductImageInline]


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    list_editable = ('order', 'is_active')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'comment')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name',)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'deal_type', 'status', 'discount_display', 'start_date', 'end_date', 'is_featured', 'product_count')
    list_filter = ('deal_type', 'status', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('status', 'is_featured')
    filter_horizontal = ('products',)
    readonly_fields = ('current_uses', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'badge_text', 'banner_image', 'is_featured')
        }),
        ('Discount Configuration', {
            'fields': ('deal_type', 'discount_percentage', 'discount_amount')
        }),
        ('Validity & Usage', {
            'fields': ('start_date', 'end_date', 'status', 'max_uses', 'current_uses')
        }),
        ('Products', {
            'fields': ('products',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def discount_display(self, obj):
        return obj.get_discount_display()
    discount_display.short_description = 'Discount'
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new deal
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
