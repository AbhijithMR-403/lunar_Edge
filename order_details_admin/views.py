from django.shortcuts import render, redirect
from order.models import Order, OrderProduct
# Create your views here.


def order_list(request):
    orders = Order.objects.select_related('user', 'shipping_address', 'payment').all()
    
    context = {
        'orders': orders
    }
    return render(request, "admin_partition/order/order_list.html", context)


def order_details(request, id):
    order = Order.objects.get(id=id)
    order_items = OrderProduct.objects.filter(order=id)
    print(order_items)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, "admin_partition/order/orders_detail.html", context)


def delivered(request, id):
    order = Order.objects.get(id=id)
    if order.order_status == 'Accepted':
        order.order_status = 'Delivered'
        order.save()
    return redirect('admin_order:order_list')
