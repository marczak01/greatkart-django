from django.shortcuts import get_object_or_404, render
from .models import Product
from carts.models import CartItem, Cart
from category.models import Category

from carts.views import _cart_id
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        #if we define url path like: "/store/shoes/"
        categories = get_object_or_404(Category, slug=category_slug)
        #if we try to get slug witch is None then we get 404 error
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        #if we do not define url path like "/store/shoes/"
        #and we only say "/store/" then we'll see all available products
        products = Product.objects.all().filter(is_available=True)
        #only products with is_available set to True will be displayed
        product_count = products.count()

    category = Category.objects.all()

    context = {
        'products': products,
        'product_count': product_count,
        'category': category,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)