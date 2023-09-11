from django.urls import path
from authenticator import views

urlpatterns = [
    path('',views.userLogin,name='userlogin'),
#     path('signup/',views.userSignup,name='usersignup'),
#     path('otp/',views.otp,name='otp'),
]