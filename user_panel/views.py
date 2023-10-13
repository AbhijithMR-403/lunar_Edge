from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from category_management.models import Category
from product_management.models import Product_Variant, Product
from .models import Cart, Cart_item
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse


def home_page(request):
    product = Product.objects.all()
    products_list = []
    for i in product:
        if Product_Variant.objects.filter(product=i):
            products_list.append(Product_Variant.objects.filter(product=i)[0])
    print(products_list)

    content = {
        "products": products_list,
        "categories": Category.objects.all(),
    }
    return render(request, "user_partition/user_page/home.html", content)


def product_page(request):
    content = {"products": Product_Variant.objects.all()}
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


def user_cart(request, slug=None):
    if not request.user.is_authenticated:
        messages.warning(request, "You needs to login first")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    user_cart, check_user_cart = Cart.objects.get_or_create(user=request.user)

    cart_items = Cart_item.objects.filter(cart_id=user_cart)
    # ^ Check any item added to cart
    # & Else return to previous page
    if cart_items.count() == 0:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    subtotal = sum(i.product_id.sale_price * i.quantity for i in cart_items)
    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": subtotal + 100,
    }
    return render(request, "user_partition/order/cart.html", context)


# ! haven't finished


def add_to_cart(request, id):
    if not request.user.is_authenticated:
        messages.warning(request, "You needs to login first")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    user_cart, check = Cart.objects.get_or_create(user=request.user)
    product = Product_Variant.objects.get(id=id)
    cart_item, check_cart_item = Cart_item.objects.get_or_create(
        product_id=product, cart_id=user_cart
    )
    cart_item.quantity += 1
    cart_item.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_cart_item(request, id):
    cart_item = Cart_item.objects.get(id=id)
    cart_item.delete()
    return redirect("user_home:user_cart")


def order(request):
    cart_user = Cart.objects.get(user=request.user)
    cart_item = Cart_item.objects.filter(cart_id=cart_user)
    cart_item.delete()
    return HttpResponse("Your order is now placed")


def plus_cart(request, slug):
    cart_user = Cart.objects.get(user=request.user)
    product = Product_Variant.objects.get(product_variant_slug=slug)
    cart_item = Cart_item.objects.get(cart_id=cart_user, product_id=product)
    cart_item.quantity += 1
    
    print('reach here akdsfajkdhfakjfjhdfj\n\n\\n\n')
    cart_item.save()
    return redirect("user_home:user_cart")


def minus_cart(request, slug):
    cart_user = Cart.objects.get(user=request.user)
    product = Product_Variant.objects.get(product_variant_slug=slug)
    cart_item = Cart_item.objects.get(cart_id=cart_user, product_id=product)
    if cart_item.quantity != 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("user_home:user_cart")
