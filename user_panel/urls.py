
from django.urls import path
from user_panel import views

app_name = 'user_home'

urlpatterns = [
    path('',views.home_page,name='home'),
    path('shop/',views.product_page,name='product'),
]