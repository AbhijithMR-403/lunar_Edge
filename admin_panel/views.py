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
    products=Product.objects.all()
    content={
        'products':products
    }
    return render(request,'admin_partition/product.html',content)


def categories(request):
    # if request.method == 'POST':
        
    categories=Category.objects.all()
    content={
        'categories':categories
    }
    return render(request,'admin_partition/category.html',content)


def admin_login(request):
    if request.method =='POST':
        email=request.POST['email']
        password=request.POST['password']
        try:
            if not Account.objects.filter(email=email).exists():
                    messages.warning(request,'No user found')
                    return redirect('admin_panel:login')
        except:
            pass
        # only needed when you are doing email validation 
    
        user = authenticate(email=email,password=password)
        if user is None:
            messages.error(request,'Invalid detailes')
            return redirect('admin_panel:login')
        else:
            if user.is_superuser:
                login(request,user)
                return redirect('admin_panel:dashboard')
            else:
                messages.error('Only for superuser')

    return render(request,'admin_partition/sign_in/login.html')


def add_categories(request):
    
    return redirect('admin_panel:categories')

def add_product(request):
    form=product_form
    if request.method =="POST":
        form=product_form(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            print(product)
            product.save()
            return redirect('admin_panel:add_product')
        else:
            return render(request,'admin_partition/addproduct.html',{'form':form})

    return render(request,'admin_partition/addproduct.html',{'form':form})