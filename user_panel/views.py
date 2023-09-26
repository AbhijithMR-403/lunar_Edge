from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from category_management.models import *
# Create your views here.

def home_page(request):
   content = {
      # 'products':Product.objects.all(),
      'categories':Category.objects.all(),
      }
   return render(request,'user_partition/user_page/home.html',content)

def product_page(request):
   pass
   content ={
      'products' : Product.objects.all()
   }
   return render(request,'user_partition/user_page/shop.html',content)

def logout_user(request):
   logout(request)
   return redirect('user_home:home')

def product_details(request,id):
   pass
   detail=Product.objects.get(id=id)
   return render(request,'user_partition/user_page/product_detail.html',{'detail':detail})