from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import Account
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
import random
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
            messages.warning(request,'Your account is blocked ')
            # Account.objects.get(email=email,is_active=False).is_active=True
            return redirect('user_partition:userlogin')
   except:
      pass
   
   user = authenticate(email=email,password=password)
   if user is None:
      messages.error(request,'Invalid detailes')
      return redirect('user_partition:userlogin')
   else:
      
      login(request,user)
      return redirect('user_home:home')
   # !till above line
      

def sent_otp(request):
   random_num=random.randint(1000,9999)
   request.session['OTP_Key']=random_num
   send_mail(
   "OTP AUTHENTICATING LUNAR_EDGE",
   f"{random_num} -OTP",
   "luttapimalayali@gmail.com",
   [request.session['email']],
   fail_silently=False,
)
   return redirect('user_partition:otp')
   
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otp(request):
   if request.user.is_authenticated:
      return redirect('user_home:home')
   user=Account.objects.get(email=request.session['email'])
   if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         messages.warning(request,'Check your otp again')
         print(request.session['OTP_Key'],request.POST['otp'])
      else:
         user.is_active=True
         user.save()
         login(request,user)
         return redirect('user_home:home')
   return render(request,'user_partition/user_authentication/otp.html')
   



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):
   if request.user.is_authenticated:
      return redirect('user_home:home')
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
   
   request.session['email']=email
   return redirect('user_partition:sent_otp')

def forgetpassword(request):
   if request.method != 'POST':
      return render(request,'user_partition/user_authentication/forgetpassword.html')
   pass1=request.POST['re_password']
   pass2=request.POST['password']
   if pass1 != pass2:
      messages.warning(request,'Both are not the same')
      return redirect('user_partition:forgetpassword')
   else:
      user=Account.objects.get(email=request.session['pemail'])
      user.set_password(pass1)
      user.save()
      return redirect('user_partition:userlogin')


def email(request):
   if request.method != "POST":
      return render(request,'user_partition/user_authentication/email.html')
   
   email=request.POST['email']
   if Account.objects.filter(email=email).exists(): 
      request.session['pemail']=email
      random_num=random.randint(1000,9999)
      request.session['POTP_Key']=random_num
      send_mail(
      "OTP AUTHENTICATING LUNAR_EDGE",
      f"{random_num} -OTP",
      "luttapimalayali@gmail.com",
      [email],
      fail_silently=False,
   )
      return redirect("user_partition:potp")
   else:
      messages.error(request,'Invalid one')
   return render(request,'user_partition/user_authentication/email.html')

def potp(request):

   if request.method != 'POST':
      return render(request,'user_partition/user_authentication/potp.html')
   
   if str(request.POST['otp'])==str(request.session['POTP_Key']):
      return redirect('user_partition:forgetpassword')
   else:
      messages.warning(request,'Invalid otp')
      return redirect('user_partition:potp')
   