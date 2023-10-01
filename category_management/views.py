from django.shortcuts import render,redirect
from .models import Category
from django.contrib import messages
# Create your views here.


# ^ Category list
def categories(request):
    
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    categories=Category.objects.all()
    content={
        'categories':categories
    }
    return render(request,'admin_partition/category.html',content)

# ^ Category add

def add_category(request):
    category_name   = request.POST['category_name']
    parent          = None if request.POST['parent'] =='None' else Category.objects.get(category_name=request.POST['parent'])
    description     = request.POST['description']
    soft_delete     = request.POST.get('soft_delete', False) != False
    image           = request.FILES['image']

    Category.objects.create(
        category_name   = category_name,
        parent          = parent,
        description     = description,
        # soft_delete     = soft_delete,
        category_img    = image,
    )
    return redirect('category:category_list')

def delete_category(request,slug):
    
    try:
        category = Category.objects.get(slug=slug)
    except ValueError:
        return redirect('category:category_list')
    category.delete()
    messages.error(request, "Category Deleted ❌")
    return redirect('category:category_list')
