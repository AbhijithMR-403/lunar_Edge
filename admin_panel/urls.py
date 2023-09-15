from django.urls import path
from admin_panel import views

app_name='admin_panel'

urlpatterns = [
    # path('',views.login,name='adminlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('product_list/',views.product_list,name='product_list'),
    # path('')
]