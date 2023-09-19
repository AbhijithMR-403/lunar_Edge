from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from admin_panel.models import *
# Create your views here.

def home_page(request):
   content = {
      'products':Product.objects.all(),
      'categories':Category.objects.all(),
      }
   return render(request,'user_partition/user_page/home.html',content)

def product_page(request):
   return render(request,'user_partition/user_page/shop.html')

def logout_user(request):
   logout(request)
   return redirect('user_home:home')