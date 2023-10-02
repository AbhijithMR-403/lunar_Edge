from django.shortcuts import render ,redirect ,HttpResponse
from authenticator.models import Account
from admin_panel.models import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.cache import cache_control


# ^ Dashboard
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # Later you can reduce this code
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    return render(request,'admin_partition/dashboard.html')


# ^ Logout
def logout_admin(request):
    logout(request)
    return redirect('admin_panel:login')


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



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    user_details=Account.objects.all().filter(is_superuser=False)
    content={
       'user_details':user_details
    }
    return render(request,'admin_partition/user_list.html',content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_unblock_user(request,id,block):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')

    try:
        user=Account.objects.get(id=id)
        user.is_active = (block == 1)
        user.save()
    except:
        pass
    return redirect('admin_panel:user_list')
