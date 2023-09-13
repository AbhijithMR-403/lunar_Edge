from django.urls import path
from authenticator import views

app_name = 'user_partition'

urlpatterns = [
    path('login/',views.user_login,name='userlogin'),
    path('signup/',views.user_signup,name='usersignup'),
    # path('otp/',views.otp,name='otp'),
    path('',views.home_page,name='home')
]