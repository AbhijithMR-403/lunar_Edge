from django.shortcuts import render,HttpResponse

# Create your views here.
def userLogin(request):
    print(request.method)
    if request.method != 'POST':
       return render(request,'user_partition/user_authentication/login.html')
    email=request.POST['email']
    password=request.POST['password']
    return HttpResponse('hello')

