from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from authenticator.models import Account, user_profile
from order.models import Order, OrderProduct
from .models import WishList
from product_management.models import Product_Variant

# ^Templates
user_profile_path = "user_partition/profile/"


def profile(request):
    try:
        user = Account.objects.get(email=request.user)
        user_extra_details, check_created = user_profile.objects.get_or_create(
            account=user)
    except Exception:
        return redirect('user_home:home')
    if request.method == 'POST':
        field_name = request.POST['name']
        value = request.POST['value']
        # user_data = Account.objects.get(email=request.user)
        setattr(user_extra_details, field_name, value)
        user_extra_details.save()
    context = {
        "user_details": user,
        "user_extra_details": user_extra_details
    }
    return render(request, f"{user_profile_path}profile.html", context)


def address(request):
    return render(request, f'{user_profile_path}address.html')


def order(request):
    order_details = Order.objects.select_related(
        'user').filter(user__email=request.user).exclude(order_status='New')
    context = {
        'order_details': order_details,
    }
    return render(request, f'{user_profile_path}order.html', context)


def wallet_profile(request):
    user = Account.objects.get(email=request.user)
    wallets, check_created = user_profile.objects.get_or_create(
        account=user)
    return render(request,
                  f'{user_profile_path}wallet.html', {'wallets': wallets})


def wishlist(request):
    products = WishList.objects.filter(user=request.user)
    context = {"products": products}
    return render(request, f'{user_profile_path}wishlist.html', context)


def order_cancel(request, id):
    wallet_balance = user_profile.objects.get(account=request.user)
    cart_detail = Order.objects.get(id=id)
    cart_detail.order_status = 'Cancelled'
    wallet_balance.wallet = float(wallet_balance.wallet)+float(cart_detail.payment.amount_paid)
    wallet_balance.save()
    cart_detail.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def order_details(request, id):
    order = Order.objects.get(id=id)
    order_details = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'order_details': order_details,
    }
    return render(request, f'{user_profile_path}order_detail.html', context)


def add_wishlist(request, id):
    product = Product_Variant.objects.get(id=id)
    if WishList.objects.filter(user=request.user, product=product).exists():
        messages.info(request, "This item is already in your wishlist")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    wishlist = WishList.objects.create(
        user=request.user, product=product)
    wishlist.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_wishlist(request, id):
    product = Product_Variant.objects.get(id=id)
    print(product, id, request.user, '\n\n\n')
    print(WishList.objects.filter(user=request.user, product=product))
    try:
        wishlist = WishList.objects.get(user=request.user, product=product)
        wishlist.delete()
    except:
        messages.warning(request, "Error")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
