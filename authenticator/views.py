from django.shortcuts import render,HttpResponse

# Create your views here.
def user_login(request):
   #  print(request.method)
   #  if request.method != 'POST':
   #     return render(request,'user_partition/user_authentication/login.html')
   #  email=request.POST['email']
   #  password=request.POST['password']
   #  return HttpResponse('hello')
   return render(request, 'user_partition/user_authentication/login.html')



def user_signup(request):
   return render(request,'user_partition/user_authentication/signup.html')



def home_page(request):
   return render(request,'user_partition/user_page/home.html')
