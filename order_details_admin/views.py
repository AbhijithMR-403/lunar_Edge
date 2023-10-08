from django.shortcuts import render
from order.models import Order, OrderProduct
# Create your views here.


def order_list(request):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, "admin_partition/order/order_list.html", context)


def order_details(request, id):
    order = Order.objects.get(id=id)
    order_items = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, "admin_partition/order/orders_detail.html", context)
