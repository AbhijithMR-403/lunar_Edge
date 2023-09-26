from django.urls import path
from admin_panel import views

app_name='admin_panel'

urlpatterns = [
    path('',views.admin_login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout_admin/',views.logout_admin,name='logout'),
    path('user_list/',views.user_list,name='user_list'),
    path('block_unblock_user/<int:id>/<int:block>',views.block_unblock_user,name='block_unblock_user'),
]