from django.shortcuts import render ,redirect ,HttpResponse
from authenticator.models import Account
from admin_panel.models import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import product_form
from django.views.decorators.cache import cache_control

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # Later you can reduce this code
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    return render(request,'admin_partition/dashboard.html')

def product_list(request):
    products=Product.objects.all()
    content={
        'products':products
    }
    return render(request,'admin_partition/product.html',content)


def logout_admin(request):
    logout(request)
    return redirect('admin_panel:login')

def categories(request):
    
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    categories=Category.objects.all()
    content={
        'categories':categories
    }
    return render(request,'admin_partition/category.html',content)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    logout(request)
    print(request.user,'\n\n\n\n')
    if request.user.is_superuser:
        print('\n\nsdfadfa\n\n\n')
        redirect('admin_panel:dashboard')
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
            print(request.user,'\n\n\n\n\n\nabove this')
            if user.is_superuser:
                login(request,user)
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request,'Only for superuser')

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