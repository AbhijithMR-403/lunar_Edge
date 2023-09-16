from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import Account
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate

# Create your views here.
def user_login(request):
   
   if request.user.is_authenticated:
      return redirect('user_home:home')
   if request.method != 'POST':
      return render(request,'user_partition/user_authentication/login.html')
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
      print("\n\n\n\n\ndadsfasd\n\n\n\n\n\n")
      messages.error(request,'Invalid detailes')
      return redirect('user_partition:userlogin')
   else:
      
      print("\n\n\n\n\ndadsfasd\n\n\n\n\n\n")
      login(request,user)
      return redirect('user_partition:otp')
      
   
   
def otp(request):
   if request.method!="POST":
      return render(request,'user_partition/user_authentication/otp.html')
   return redirect('user_home:home')
   


def user_signup(request):
   if request.method != 'POST':
      return render(request,'user_partition/user_authentication/signup.html')
   username = request.POST['name']
   email = request.POST['email']
   password1 = request.POST['password1']
   password2 = request.POST['password2']
   
   if not username and not email and not password1 and not password2:
         messages.warning(request,'Type something to register')
         return redirect('user_partition:usersignup')

   if not username:
      messages.warning(request,'Type your name')
      return redirect('user_partition:usersignup')
   if not email or '@' not in email:
      messages.warning(request,'Invalid email')
      return redirect('user_partition:usersignup')
   if not password1 or len(password1)<4:
      messages.warning(request,'Type more character\' for password')
      return redirect('user_partition:usersignup')
   if not password2:
      messages.warning(request,'Type this re-password')
      return redirect('user_partition:usersignup')

   try:
      if Account.objects.get(username=username):
         messages.warning(request,'Username is already taken')
         return redirect('user_partition:usersignup')
   except Exception:
      pass

   try:
      if Account.objects.get(email=email):
         messages.warning(request,'Email is already taken')
         return redirect('user_partition:usersignup')
   except Exception:
      pass

   if password1 != password2:
      messages.warning(request,'Password is wrong')
      return redirect('user_partition:usersignup')
 
   Myuser=Account.objects.create_user(username=username,email=email,password=password1)
   # Myuser.save()
   return redirect('user_partition:userlogin')

