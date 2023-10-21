from django.urls import path
from user_panel import views

app_name = 'user_home'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('shop/', views.product_page, name='shop'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('product_details/<str:slug>',
         views.product_details, name='product_details'),
    path('category/<int:id>/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('sort_by/<str:att>', views.sort_by, name='sort_by'),
]
