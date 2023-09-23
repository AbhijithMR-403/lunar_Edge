from django.shortcuts import render ,redirect ,HttpResponse
from authenticator.models import Account
from admin_panel.models import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import product_form
from django.views.decorators.cache import cache_control


# ^ Dashboard
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # Later you can reduce this code
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    return render(request,'admin_partition/dashboard.html')


# ^ List product
def product_list(request):
    products=Product.objects.all()
    content={
        'products':products
    }
    return render(request,'admin_partition/product.html',content)


# ^ Logout
def logout_admin(request):
    logout(request)
    return redirect('admin_panel:login')


# ^ Category list
def categories(request):
    
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    categories=Category.objects.all()
    content={
        'categories':categories
    }
    return render(request,'admin_partition/category.html',content)



#  ^ admin login

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
            messages.warning(request,'Invalid detailes')
            return redirect('admin_panel:login')
        else:
            if user.is_superuser:
                login(request,user)
                return redirect('admin_panel:dashboard')
            else:
                messages.warning(request,'Only for superuser')

    return render(request,'admin_partition/sign_in/login.html')



def add_categories(request):
    if request.method != 'POST':
        return redirect('admin_panel:categories')
    name=request.POST['product_name']
    parent=request.POST['parent']
    description=request.POST['description']
    soft_delete = (request.POST.get('soft_delete', False)) != False
    image=None
    if request.FILES:
        image=request.FILES['image']
    print(soft_delete,'\n\n\n\n\ndsfsdfd')
    print(Category.objects.get(category_name=parent),'\n\n\n\n\ndsfsdfd')
    category = Category.objects.create(category_name    = name,
                                       parent           = Category.objects.get(category_name=parent),
                                       description      = description,
                                       soft_deleted     = soft_delete,
                                       category_img     = image
                                       )
    category.save()
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


def user_list(request):
   user_details=Account.objects.all().filter(is_superuser=False)
   content={
       'user_details':user_details
   }
   return render(request,'admin_partition/user_list.html',content)


def block_unblock_user(request,id,block):
    try:
        user=Account.objects.get(id=id)
        user.is_active = (block == 1)
        user.save()
    except:
        pass
    return redirect('admin_panel:user_list')
