from curses import keyname
from django.shortcuts import get_object_or_404, render
from .models import Product, Variation
from carts.models import CartItem, Cart
from category.models import Category
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        #if we define url path like: "/store/shoes/"
        categories = get_object_or_404(Category, slug=category_slug)
        #if we try to get slug witch is None then we get 404 error
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        #if we do not define url path like "/store/shoes/"
        #and we only say "/store/" then we'll see all available products
        products = Product.objects.all().filter(is_available=True).order_by('id')
        #only products with is_available set to True will be displayed
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    variations = Variation.objects.all()

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'variations': variations,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET: #check if keyword present in url
        keyword = request.GET['keyword'] #if present in url then store its value inside of keyword variable
        if keyword: #if keyword is not blank ..if not keyword=" "
            #store products ordered by date and filter by keyword. if keyword is in description of product
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context={
        'products': products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)



