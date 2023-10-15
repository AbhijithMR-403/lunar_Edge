from django.urls import path
from user_panel import views

app_name = 'user_home'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('shop/', views.product_page, name='shop'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('product_details/<str:slug>',
         views.product_details, name='product_details'),
]
