from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .form import addressbook_form
from authenticator.models import Account, AddressBook
from user_panel.models import Cart, Cart_item
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
    cart_id = Cart.objects.get(user=request.user)
    cart_details = Cart_item.objects.select_related(
        "cart_id").filter(cart_id=cart_id)
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
        print(request.POST['payment'])
    return redirect('order:checkout')