from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('add_brand/', views.add_brand, name='add_brand'),
    path('add_attribute/', views.add_attribute, name='add_attribute'),
    path('add_attribute_value/', views.add_attribute_value,
         name='add_attribute_value'),
    path('product_list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_product_variant/', views.add_product_variant,
         name='add_product_variant'),
    path('delete_product/<str:slug>/',
         views.delete_product, name='delete_product'),
    path('edit_product/<str:slug>/', views.edit_product, name='edit_product'),
]
