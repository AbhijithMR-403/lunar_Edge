from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('order/', views.order, name='order'),
    path('wallet/', views.wallet_profile, name='wallet'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('order_cancel/', views.order_cancel, name='order_cancel'),
    path('order_details/', views.order_details, name='order_details'),
]
