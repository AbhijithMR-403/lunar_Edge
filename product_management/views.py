from django.shortcuts import render,redirect
from .models import Product,Product_Variant
from .forms import product_form,brand_form,attribute_name_form,attribute_value_form,product_variant_form
# Create your views here.

# ^ List product
def product_list(request):
    content={
   'products':Product_Variant.objects.all()
   }
    return render(request,'admin_partition/product.html',content)

# ^ Add product
def add_product(request):
    form=product_form
    if request.method =="POST":
        form=product_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product:add_product')
        else:
            return render(request,'admin_partition/addproduct.html',{'form':form})
    return render(request,'admin_partition/addproduct.html',{'form':form})


# ^ Add brand
def add_brand(request):
    form=brand_form
    if request.method == 'POST':
        form=brand_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:add_brand')
        else:
            return render(request,'admin_partition/addfield.html',{'form':form})
    return render(request,'admin_partition/addfield.html',{'form':form})


# ^ Add attribute
def add_attribute(request):
    form=attribute_name_form
    if request.method == 'POST':
        form=attribute_name_form(request.POST)
        if form.is_valid():
            attribute = form.save(commit=False)
            print(attribute)
            attribute.save()
            return redirect('product:add_attribute')
        else:
            return render(request,'admin_partition/addfield.html',{'form':form})
    return render(request,'admin_partition/addfield.html',{'form':form})


# ^ Add attribute values
def add_attribute_value(request):
    form=attribute_value_form
    if request.method == 'POST':
        form=attribute_value_form(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            print(product)
            product.save()
            return redirect('product:add_attribute_value')
        else:
            return render(request,'admin_partition/addfield.html',{'form':form})
    return render(request,'admin_partition/addfield.html',{'form':form})

# ^ Add product variant
def add_product_variant(request):
    form = product_variant_form
    if request.method == 'POST':
        
        form=product_variant_form(request.POST , request.FILES)
        print(form)
        if form.is_valid():
            product = form.save()
            # print(product)
            # product.save_m2m()
            return redirect('product:add_product_variant')
        else:
            return render(request,'admin_partition/addfield.html',{'form':form})
    return render(request,'admin_partition/addfield.html',{'form':form})
