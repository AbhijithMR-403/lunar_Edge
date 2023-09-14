
from django.urls import path
from user_panel import views

app_name = 'user_home'

urlpatterns = [
    path('',views.home_page,name='home')
]