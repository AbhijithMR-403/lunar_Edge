from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from product_management.models import Product_Variant
from user_panel.models import Cart, Cart_item
from django.contrib import messages
from .models import Coupon
from django.http import HttpResponseRedirect


# Create your views here.

def user_cart(request, slug=None):
    request.session['wallet'] = False
    if not request.user.is_authenticated:
        messages.warning(request, "You needs to login first")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    user_cart, check_user_cart = Cart.objects.get_or_create(user=request.user)

    cart_items = Cart_item.objects.filter(cart_id=user_cart)
    # ^ Check any item added to cart
    # & Else return to previous page
    if cart_items.count() == 0:
        if (request.META.get('HTTP_REFERER')[-5:] == 'cart/'):
            return redirect("user_home:home")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    discount = 0
    subtotal = sum(i.product_id.sale_price * i.quantity for i in cart_items)
    total = subtotal + 100
    if user_cart.coupon:
        if user_cart.coupon.minimum_amount < total:
            discount = user_cart.coupon.discount

    # request.session["cart_total"] = str(subtotal + 100)
    context = {
        "user_cart": user_cart,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": subtotal + 100 - discount,
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


def add_coupon(request):
    coupon_code = Coupon.objects.filter(code=request.POST['coupon'])
    print(coupon_code)
    if coupon_code.exists():
        user_cart = Cart.objects.get(user=request.user)
        user_cart.coupon = coupon_code[0]
        user_cart.save()
    return redirect('user_cart:user_cart')


def remove_coupon(request):
    user_cart = Cart.objects.get(user=request.user)
    user_cart.coupon = None
    user_cart.save()
    return redirect('user_cart:user_cart')
