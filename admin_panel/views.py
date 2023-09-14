from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request,'admin_partition/dashboard.html')

def product_list(request):
    return render(request,'admin_partition/product.html')