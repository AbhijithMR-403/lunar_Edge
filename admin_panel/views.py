from django.shortcuts import render ,redirect ,HttpResponse
from admin_panel.models import *

# Create your views here.
def dashboard(request):
    return render(request,'admin_partition/dashboard.html')

def product_list(request):
    return render(request,'admin_partition/product.html')


def categories(request):
    categories=Category.objects.all()
    content={
        'categories':categories
    }
    return render(request,'admin_partition/category.html',content)


def login(request):
    return render(request,'admin_partition/login.html')


def add_categories(request):
    
    return redirect('admin_panel:categories')