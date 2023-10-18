from django.shortcuts import render, redirect
from authenticator.models import Account, user_profile
from order.models import Order
# from .models import wallet
from order.models import Order, OrderProduct
from django.http import HttpResponseRedirect

# Create your views here.


def profile(request):
    print(request.user.last_login)
    try:
        user = Account.objects.get(email=request.user)
        user_extra_details, check_created = user_profile.objects.get_or_create(account=user)
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
    return render(request, "user_partition/profile/profile.html", context)


def address(request):
    return render(request, 'user_partition/profile/address.html')


def order(request):
    order_details = Order.objects.select_related('user').filter(user__email=request.user)
    context = {
        'order_details': order_details,
    }
    return render(request, 'user_partition/profile/order.html', context)


def wallet_profile(request):
    user = Account.objects.get(email=request.user)
    wallets, check_created = user_profile.objects.get_or_create(account=user)
    return render(request,
                  'user_partition/profile/wallet.html', {'wallets': wallets})


def wishlist(request):
    return render(request, 'user_partition/profile/wishlist.html')


def order_cancel(request, id):
    wallet_balance = user_profile.objects.get(account=request.user)
    cart_detail = Order.objects.get(id=id)
    cart_detail.order_status = 'Cancelled'
    wallet_balance.wallet = float(cart_detail.payment.amount_paid)
    wallet_balance.save()
    cart_detail.save()
    print('reacjed here')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def order_details(request, id):
    order = Order.objects.get(id=id)
    order_details = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'order_details': order_details,
    }
    return render(request, 'user_partition/profile/order_detail.html', context)
