from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from category_management.models import Category
from product_management.models import Product_Variant, Product
from .models import Cart, Cart_item, Banner
from django.db.models import Q
from django.contrib import messages

# ^Template path
user_page = "user_partition/user_page/"


def home_page(request):
    product = Product.objects.all()
    banners = Banner.objects.all()
    products_list = []
    for i in product:
        if Product_Variant.objects.filter(product=i):
            products_list.append(Product_Variant.objects.filter(product=i)[0])
    content = {
        "banners": banners,
        "products": products_list,
        "categories": Category.objects.all(),
    }
    return render(request, f"{user_page}home.html", content)


def product_page(request):
    products = Product_Variant.objects.all()
    if 'filter' in request.session:
        pk_key = request.session['filter']
        products = Product_Variant.objects.filter(id__in=pk_key)
    else:
        messages.warning(request, 'No such product')
    cart_count = 0
    categories = Category.objects.all()
    try:
        cart = Cart.objects.get(user=request.user)
        cart_count = Cart_item.objects.filter(cart_id=cart).count()
    except Exception:
        cart_count = 0
    if 'sort_by' in request.session:
        print(products)
        print(request.session['sort_by'])
        products = products.order_by(request.session['sort_by'])
    content = {
        "products": products,
        "cart_count": cart_count,
        "categories": categories,
    }
    return render(request, f"{user_page}shop.html", content)


def logout_user(request):
    logout(request)
    return redirect("user_home:home")


def product_details(request, slug):
    single_product_variant = (
        Product_Variant.objects.select_related("product")
        .prefetch_related("attributes")
        .get(product_variant_slug=slug, is_active=True)
    )
    variants = Product_Variant.objects.select_related("product").filter(
        product=single_product_variant.product
    )
    detail = Product_Variant.objects.get(product_variant_slug=slug)
    context = {
        "variants": variants,
        "detail": detail,
    }
    return render(request, f"{user_page}product_detail.html", context)


# !Delete if not needed
def order(request):
    cart_user = Cart.objects.get(user=request.user)
    cart_item = Cart_item.objects.filter(cart_id=cart_user)
    cart_item.delete()
    return HttpResponse("Your order is now placed")


def category(request, id):
    try:
        parent_category = Category.objects.get(id=id)
        products = Product.objects.filter(
            Q(product_catg=parent_category) |
            Q(product_catg__parent=parent_category))
        product_variants = [i.id for i in Product_Variant.objects.filter(product__in=products)]
    except Exception:
        product_variants = [i.id for i in Product_Variant.objects.all()]

    request.session['filter'] = product_variants
    return redirect('user_home:shop')


def search(request):
    if request.method == "POST":
        query = request.POST["search"]
        print('hello')
        products = Product_Variant.objects.filter(description__icontains=query)
        product_variants = [i.id for i in products]
        request.session['filter'] = product_variants
        print(product_variants)
    return redirect('user_home:shop')


def sort_by(request, att):
    request.session['sort_by'] = att
    return redirect('user_home:shop')
