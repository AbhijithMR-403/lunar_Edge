from django.urls import path
from admin_panel import views

app_name='admin_panel'

urlpatterns = [
    path('',views.admin_login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('product_list/',views.product_list,name='product_list'),
    path('categories/',views.categories,name='categories'),
    path('add_categories/',views.add_categories,name='add_categories'),
    path('add_product/',views.add_product,name='add_product'),
]