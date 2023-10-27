from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('add_address/', views.add_address, name='add_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('default_address/<int:id>',
          views.default_address, name="default_address"),
    path('delete_address/<int:id>', views.delete_address, name="delete_address"),
    path('place_order', views.place_order, name="place_order"),
    path('cash_on_delivery', views.cash_on_delivery, name="cash_on_delivery"),
    path('payment_gateway', views.payment_gateway, name='payment_gateway'),
    path('success', views.success, name='success'),
    path('order_success/', views.order_success, name='order_success'),
    path('wallet_calculation/',
         views.wallet_calculation, name='wallet_calculation'),
]
