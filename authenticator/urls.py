from django.urls import path
from authenticator import views

app_name = 'user_partition'

urlpatterns = [
    path('login/',views.user_login,name='userlogin'),
    path('signup/',views.user_signup,name='usersignup'),
    path('otp/',views.otp,name='otp'),
    path('sent_otp/',views.sent_otp,name='sent_otp'),
    path('forget_password/',views.forgetpassword,name='forgetpassword'),
    path('email/',views.email,name='email'),
    path('potp/',views.potp,name='potp'),
]