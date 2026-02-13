from .models import Cart

def cart_context(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(customer__user=request.user)
            cart_count = sum(item.quantity for item in cart_items)
        except:
            pass
    return {'cart_count': cart_count}