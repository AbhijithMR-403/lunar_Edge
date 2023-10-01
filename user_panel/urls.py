from django.urls import path
from user_panel import views

app_name = 'user_home'

urlpatterns = [
    path('',views.home_page,name='home'),
    path('shop/',views.product_page,name='shop'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('product_details/<str:slug>',views.product_details,name='product_details'),
    path('cart/',views.user_cart,name='user_cart'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('profile/',views.profile,name='user_profile'),
    path('checkout/',views.checkout,name='checkout')
]