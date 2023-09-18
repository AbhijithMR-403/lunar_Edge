from django.shortcuts import render ,redirect ,HttpResponse
from authenticator.models import Account
from admin_panel.models import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import product_form

# Create your views here.
def dashboard(request):
    return render(request,'admin_partition/dashboard.html')

def product_list(request):
    return render(request,'admin_partition/product.html')


def categories(request):
    # if request.method == 'POST':
        
    categories=Category.objects.all()
    content={
        'categories':categories
    }
    return render(request,'admin_partition/category.html',content)


def login(request):
    email=request.POST['email']
    password=request.POST['password']
    email=request.POST['email']
    password=request.POST['password']
    try:
       if not Account.objects.filter(email=email).exists():
             messages.warning(request,'No user found')
             return redirect('user_partition:userlogin')
    except:
       pass
    # only needed when you are doing email validation 
    try:
       if Account.objects.filter(email=email,is_active=False).exists():
             messages.warning(request,'You have to active first ')
             return redirect('user_partition:userlogin')
    except:
       pass
    
    user = authenticate(email=email,password=password)
    if user is None:
       messages.error(request,'Invalid detailes')
       return redirect('user_partition:userlogin')
    else:
       login(request,user)
       return redirect('user_partition:otp')
    # return render(request,'admin_partition/sign_in/login.html')


def add_categories(request):
    
    return redirect('admin_panel:categories')

def add_product(request):
    form=product_form
    return render(request,'admin_partition/addproduct.html',{'form':form})