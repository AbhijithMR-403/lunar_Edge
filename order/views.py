from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.conf import settings
import uuid
import razorpay

from authenticator.models import Account, AddressBook, user_profile
from .form import addressbook_form
from user_panel.models import Cart, Cart_item
from .models import Payment, Order, OrderProduct

# ^ Template Path
order_path = "user_partition/order/"


def add_address(request):
    if request.method == "POST":
        form = addressbook_form(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
        else:
            print(form.non_field_errors())
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
 
  
def checkout(request):
    wallet_check = request.session['wallet']
    if (request.META.get('HTTP_REFERER')[-9:] == 'checkout/'):
        print('you are in this checkout page here in checkout')

    try:
        cart_id = Cart.objects.get(user=request.user)
    except Exception:
        return redirect('user_home:home')
    cart_details = Cart_item.objects.select_related(
        "cart_id").filter(cart_id=cart_id)
    wallet_obj, check = user_profile.objects.get_or_create(account=request.user)
    if cart_details.count() == 0:
        messages.warning(request, 'Add Product To Cart')
        return redirect('user_cart:user_cart')
    subtotal = sum(i.product_id.sale_price * i.quantity for i in cart_details)
    cart_id.subtotal = subtotal
    cart_id.save()
    addresses = AddressBook.objects.filter(user=request.user, is_active=True)
    discount = 0
    if cart_id.coupon:
        discount = cart_id.coupon.discount
    total = subtotal + 100 - discount
    context = {
        "wallet": wallet_obj.wallet,
        "cart_id": cart_id,
        "total": total,
        "subtotal": subtotal,
        "cart_details": cart_details,
        "addresses": addresses,
        "wallet_check": wallet_check,
    }
    return render(request, f"{order_path}checkout.html", context)


def default_address(request, id):
    address = AddressBook.objects.get(id=id)
    address.is_default = True
    address.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_address(request, id):
    address = AddressBook.objects.get(id=id)
    address.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def place_order(request):

    if request.method == "POST":
        # ^ sub total amount
        cart_items = Cart_item.objects.select_related('cart_id').filter(
            cart_id__user=request.user)
        subtotal = sum(i.product_id.sale_price *
                       i.quantity for i in cart_items)
        
        # ^ Adding wallet amt if any
        user_wallet = user_profile.objects.get(account=request.user).wallet
        wallet = 0
        if request.session['wallet']:
            if (subtotal+100) < float(user_wallet):
                wallet = subtotal
            else:
                wallet = float(user_wallet)
        user = Account.objects.get(email=request.user)
        try:
            address = AddressBook.objects.get(user=user, is_default=True)
        except Exception:
            messages.warning(request, 'Please Set Default Shipping Address')
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        order_id = int(uuid.uuid4().hex[:5], 16)
        request.session['cart_id'] = order_id
        discount = 0
        if Cart.objects.get(user=request.user).coupon:
            discount = Cart.objects.get(user=request.user).coupon.discount

        # ^ Payment table
        payment_object = Payment.objects.create(
            user=user, payment_order_id=order_id,
            amount_paid=subtotal+100-discount-wallet, payment_status='PENDING')

        # ^ Order details
        order_object = Order.objects.create(
            user=user, payment=payment_object, order_number=order_id,
            shipping_address=address, order_total=subtotal,
            additional_discount=discount, wallet_discount=wallet
        )
        order_object.save()
        if request.POST['payment'] == 'COD' or 'razorpay':
            payment_object.payment_method = request.POST['payment']
            payment_object.save()
            return redirect('order:payment_gateway')
        else:
            return HttpResponse('This is not available')
    return redirect('order:checkout')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_gateway(request):
    order_id = request.session['cart_id']

    # ^ Payment method
    payment_method = Payment.objects.get(payment_order_id=order_id)
    if payment_method.payment_status == 'SUCCESS':
        return redirect("user_home:home")
    Total_amount = float(payment_method.amount_paid)

    # #  ^order details to add discound wallet
    # order_details = Order.objects.get(order_number=order_id)
    # order_details.additional_discount += wallet_discount
    # order_details.save()
    # ^ Razor pay
    if payment_method.payment_method == 'razorpay':
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create({
            'amount': Total_amount*100, 'currency': 'INR', 'payment_capture': 1})
        payment_method.payment_id = payment['id']
        payment_method.save()

    # ^Address
    address = AddressBook.objects.select_related('user').get(
        user__email=request.user, is_default=True)
    context = {
        'address': address,
        'payment_method': payment_method,
        'Total_amount': Total_amount
    }
    return render(request, f'{order_path}payment_gateway.html', context)


def success(request):
    user = request.GET['user']
    user = Account.objects.get(email=user)
    cart_items = Cart_item.objects.select_related('cart_id').filter(
        cart_id__user=user)
    order_id = request.GET['order_id']

    # ^ Payment table
    payment_object = Payment.objects.get(payment_order_id=order_id)
    payment_object.payment_status = 'SUCCESS'
    payment_object.save()

    # ^ Order details
    order_object = Order.objects.get(order_number=order_id)
    order_object.order_status = 'Accepted'
    order_object.save()
    for cart_item in cart_items:
        quantity = cart_item.quantity
        product = cart_item.product_id
        price = cart_item.product_id.sale_price
        ordered_product = OrderProduct.objects.create(
            order=order_object, user=user, product=product,
            quantity=quantity, product_price=price
        )
        ordered_product.save()

    try:
        cart_item = Cart.objects.get(user=user)
        cart_item.delete()
        return redirect('order:order_success')
    except:
        return HttpResponse("Cart does not exist for the current user.")


def order_success(request):
    user_order = Order.objects.get(order_number=request.session['cart_id'])
    order_items = OrderProduct.objects.filter(order=user_order)
    content = {
        'user_order': user_order,
        'order_items': order_items,
    }
    return render(request, f'{order_path}order_success.html', content)


def wallet_calculation(request):
    print('you can reach here')
    user = user_profile.objects.get(account=request.user)
    if user.wallet == 0:
        return JsonResponse({'check': False})
    
    if request.POST['isChecked'] == 'false':
        request.session['wallet'] = False
        return JsonResponse({'check': False})
    
    total = float(request.POST['total'])
    request.session['wallet'] = True

    if total < float(user.wallet):
        wallet_balance = float(user.wallet) - total + 100
        wallet_use = total - 100
        print(wallet_use)
        return JsonResponse({
            'check': True, 'balance': str(wallet_balance),
            'wallet_use': str(wallet_use), "total_a": '100'})
    else:
        total_balance = total - float(user.wallet)
        return JsonResponse({
            'check': True, 'total_a': str(total_balance), 'wallet_use': str(user.wallet)})
