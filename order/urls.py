from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('add_address/', views.add_address, name='add_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('default_address/<int:id>', views.default_address, name="default_address"),
    path('delete_address/<int:id>', views.delete_address, name="delete_address"),
    path('place_order', views.place_order, name="place_order"),
    path('cash_on_delivery', views.cash_on_delivery, name="cash_on_delivery"),
    path('razor_pay', views.razor_pay, name="razor_pay"),
]
