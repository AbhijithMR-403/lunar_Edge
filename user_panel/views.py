from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from category_management.models import Category
from product_management.models import Product_Variant, Product
from .models import Cart, Cart_item, Banner
from django.contrib import messages
from django.http import HttpResponseRedirect


def home_page(request):
    product = Product.objects.all()
    banners = Banner.objects.all()
    print(banners.values())
    products_list = []
    for i in product:
        if Product_Variant.objects.filter(product=i):
            products_list.append(Product_Variant.objects.filter(product=i)[0])
    print(products_list)
    cart_count = 0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_count = Cart_item.objects.filter(cart_id=cart).count()
    except Exception:
        cart_count = 0
    content = {
        "banners": banners,
        "cart_count": cart_count,
        "products": products_list,
        "categories": Category.objects.all(),
    }
    return render(request, "user_partition/user_page/home.html", content)


def product_page(request):
    cart_count = 0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_count = Cart_item.objects.filter(cart_id=cart).count()
    except Exception:
        cart_count = 0
    content = {
        "products": Product_Variant.objects.all(),
        "cart_count": cart_count,
               }
    return render(request, "user_partition/user_page/shop.html", content)


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
    return render(request, "user_partition/user_page/product_detail.html", context)


# !Delete if not needed
def order(request):
    cart_user = Cart.objects.get(user=request.user)
    cart_item = Cart_item.objects.filter(cart_id=cart_user)
    cart_item.delete()
    return HttpResponse("Your order is now placed")
