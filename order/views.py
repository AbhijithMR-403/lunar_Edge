from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from .form import addressbook_form
from authenticator.models import Account, AddressBook
from user_panel.models import Cart, Cart_item
from .models import Payment, Order, OrderProduct
from django.contrib import messages
import uuid
# Create your views here.


def add_address(request):
    if request.method == "POST":
        form = addressbook_form(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
        else:
            print(form.errors)
            print(form.data)
            print(form.cleaned_data)
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
        if request.POST['payment'] == 'COD':
            return redirect('order:cash_on_delivery')
        elif request.POST['payment'] == 'Razor_pay':
            return redirect('order:razor_pay')
        else:
            return HttpResponse('This is not available')
    return redirect('order:checkout')


def cash_on_delivery(request):
    cart_items = Cart_item.objects.select_related('cart_id').filter(
        cart_id__user=request.user)
    order_id = int(uuid.uuid4().hex[:5], 16)
    user = Account.objects.get(email=request.user)
    address = AddressBook.objects.get(user=user, is_default=True)
    # ^Total amount 
    # Excluding the delevery charge
    subtotal = sum(i.product_id.sale_price * i.quantity for i in cart_items)

    # ^ Payment table
    payment_object = Payment.objects.create(
        user=user, payment_order_id=order_id, payment_method='COD',
        amount_paid=subtotal+100, payment_status='SUCCESS')
    payment_object.save()

    # ^ Order details
    order_object = Order.objects.create(
        user=user, payment=payment_object, order_number=order_id,
        shipping_address=address, order_total=subtotal, order_status='Accepted'
        )
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
    Cart.objects.get(user=user).delete()

    return HttpResponse('you have succesfully make cash on delivery')


def razor_pay(request):
    return HttpResponse('You are being redirected to Razor Pay')
