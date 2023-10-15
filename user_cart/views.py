from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from product_management.models import Product_Variant
from user_panel.models import Cart, Cart_item
from django.contrib import messages
from .models import Coupon
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers


# Create your views here.

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
    return redirect("user_cart:user_cart")


def plus_cart(request, slug):
    cart_user = Cart.objects.get(user=request.user)
    product = Product_Variant.objects.get(product_variant_slug=slug)
    cart_item = Cart_item.objects.get(cart_id=cart_user, product_id=product)
    cart_item.quantity += 1
    print('reach here akdsfajkdhfakjfjhdfj\n\n\\n\n')
    cart_item.save()
    return redirect("user_cart:user_cart")


def minus_cart(request, slug):
    cart_user = Cart.objects.get(user=request.user)
    product = Product_Variant.objects.get(product_variant_slug=slug)
    cart_item = Cart_item.objects.get(cart_id=cart_user, product_id=product)
    if cart_item.quantity != 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("user_cart:user_cart")
