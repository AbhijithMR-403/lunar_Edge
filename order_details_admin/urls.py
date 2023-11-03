from django.urls import path
from . import views

app_name = 'admin_order'

urlpatterns = [
    path("order_list/", views.order_list, name="order_list"),
    path("order_details/<int:id>", views.order_details, name="order_details"),
    path("delivered/<int:id>", views.delivered, name="delivered"),
]
