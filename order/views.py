from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from .form import addressbook_form
from authenticator.models import Account, AddressBook
from user_panel.models import Cart, Cart_item
from .models import Payment, Order, OrderProduct
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.conf import settings
import uuid
import razorpay

# Create your views here.


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
    try:
        cart_id = Cart.objects.get(user=request.user)
    except Exception:
        return redirect('user_home:home')
    cart_details = Cart_item.objects.select_related(
        "cart_id").filter(cart_id=cart_id)
    if cart_details.count() == 0:
        messages.warning(request, 'Add Product To Cart')
        return redirect('user_home:user_cart')
    subtotal = sum(i.product_id.sale_price * i.quantity for i in cart_details)
    addresses = AddressBook.objects.filter(user=request.user)
    context = {
        "total": subtotal + 100,
        "subtotal": subtotal,
        "cart_details": cart_details,
        "addresses": addresses,
    }
    return render(request, "user_partition/order/checkout.html", context)


def default_address(request, id):
    # if not request.session['default']:
    address = AddressBook.objects.get(id=id)
    address.is_default = True
    address.save()
    print(address, '\n\n\n\n\n')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_address(request, id):
    address = AddressBook.objects.get(id=id)
    address.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def place_order(request):
    if request.method == "POST":
        user = Account.objects.get(email=request.user)
        address = AddressBook.objects.get(user=user, is_default=True)
        cart_items = Cart_item.objects.select_related('cart_id').filter(
            cart_id__user=request.user)
        subtotal = sum(i.product_id.sale_price * i.quantity for i in cart_items)
        order_id = int(uuid.uuid4().hex[:5], 16)
        # ^ Payment table
        payment_object = Payment.objects.create(
            user=user, payment_order_id=order_id,
            amount_paid=subtotal+100, payment_status='PENDING')

        # ^ Order details
        order_object = Order.objects.create(
            user=user, payment=payment_object, order_number=order_id,
            shipping_address=address, order_total=subtotal
            )
        order_object.save()

        request.session['cart_id'] = order_id
        if request.POST['payment'] == 'COD' or 'razorpay':
            payment_object.payment_method = request.POST['payment']
            payment_object.save()
            return redirect('order:payment_gateway')
        else:
            return HttpResponse('This is not available')
    return redirect('order:checkout')


def cash_on_delivery(request):
    cart_items = Cart_item.objects.select_related('cart_id').filter(
        cart_id__user=request.user)
    order_id = request.session['cart_id']
    user = Account.objects.get(email=request.user)

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
    cart = Cart.objects.get(user=user)
    print(cart, '\n\n\n\n\n')
    cart.delete()
    return redirect('order:order_success')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_gateway(request):
    order_id = request.session['cart_id']
    print(order_id)
    # ^ Payment method
    payment_method = Payment.objects.get(payment_order_id=order_id)
    if payment_method.payment_status == 'SUCCESS':
        return redirect("user_home:home")

    Total_amount = float(payment_method.amount_paid)
    # ^ Razor pay
    if payment_method.payment_method == 'razorpay':
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create({'amount': Total_amount,
                                       'currency': 'INR', 'payment_capture': 1})
        payment_method.payment_id = payment['id']
        payment_method.save()
        print(payment)

    # ^Address
    address = AddressBook.objects.select_related('user').get(
        user__email=request.user, is_default=True)
    print(payment_method.payment_method)
    context = {
        'address': address,
        'payment_method': payment_method,
        'Total_amount': Total_amount
    }
    return render(request, 'user_partition/order/payment_gateway.html', context)


def success(request):
    # order_id = request.GET['order_id']
    # status = Payment.objects.get(payment_order_id=order_id)
    # status.payment_status = 'success'
    # status.save()
    # print(status)
    user = Account.objects.get(email=request.user)
    # cart_items = Cart_item.objects.select_related('cart_id').filter(
    #     cart_id__user=user)
    cart_items = Cart_item.objects.filter(cart_id=user)
    print(cart_items)
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
        print(cart_item)
        quantity = cart_item.quantity
        product = cart_item.product_id
        price = cart_item.product_id.sale_price
        ordered_product = OrderProduct.objects.create(
            order=order_object, user=user, product=product,
            quantity=quantity, product_price=price
            )
        ordered_product.save()
    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    print('dsafjdfkjfkj', Cart.objects.filter(user=user))
    Cart.objects.get(user=user).delete()
    return redirect('order:order_success')


def order_success(request):
    return render(request, 'user_partition/order/order_success.html')
