from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0 #first we need to define this variable
    if 'admin' in request.path: #if admin then don't show it
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)) #filter Cart objects by cart_id
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)