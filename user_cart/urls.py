from django.urls import path
from user_cart import views

app_name = 'user_cart'

urlpatterns = [
    path('cart/', views.user_cart, name='user_cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart_item/<int:id>/',
         views.delete_cart_item, name='delete_cart_item'),
    path('plus_cart/<str:slug>/', views.plus_cart, name='plus_cart'),
    path('minus_cart/<str:slug>/', views.minus_cart, name='minus_cart'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
]
