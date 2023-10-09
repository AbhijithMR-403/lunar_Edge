from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('order/', views.order, name='order'),
    path('wallet/', views.wallet_profile, name='wallet'),
    path('wishlist/', views.wishlist, name='wishlist'),
]
