from .models import Cart


def cart_context(request):
    """Add cart to all templates"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {
            'cart': cart,
            'cart_count': cart.total_items
        }
    return {
        'cart': None,
        'cart_count': 0
    }
