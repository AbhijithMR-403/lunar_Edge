from django.shortcuts import render, redirect
from .models import Product_Variant
from .forms import product_form, brand_form, attribute_name_form
from .forms import attribute_value_form, product_variant_form
from django.contrib import messages


# ^ List product
def product_list(request):
    content = {
        'products': Product_Variant.objects.all()
    }
    return render(request, 'admin_partition/product.html', content)


# ^ Add product
def add_product(request):
    form = product_form
    if request.method == "POST":
        form = product_form(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'admin_partition/addproduct.html',
                          {'form': form})
        form.save()
        return redirect('product:add_product')
    return render(request, 'admin_partition/addproduct.html', {'form': form})


# ^ Add brand
def add_brand(request):
    form = brand_form
    if request.method == 'POST':
        form = brand_form(request.POST)
        if not form.is_valid():
            return render(request, 'admin_partition/addfield.html',
                          {'form': form})
        form.save()
        return redirect('product:add_brand')
    return render(request, 'admin_partition/addfield.html', {'form': form})


# ^ Add attribute
def add_attribute(request):
    form = attribute_name_form
    if request.method == 'POST':
        form = attribute_name_form(request.POST)
        if not form.is_valid():
            return render(request, 'admin_partition/addfield.html',
                          {'form': form})
        attribute = form.save(commit=False)
        print(attribute)
        attribute.save()
        return redirect('product:add_attribute')
    return render(request, 'admin_partition/addfield.html', {'form': form})


# ^ Add attribute values
def add_attribute_value(request):
    form = attribute_value_form
    if request.method == 'POST':
        form = attribute_value_form(request.POST)
        if not form.is_valid():
            return render(request, 'admin_partition/addfield.html',
                          {'form': form})
        product = form.save(commit=False)
        print(product)
        product.save()
        return redirect('product:add_attribute_value')
    return render(request, 'admin_partition/addfield.html', {'form': form})


# ^ Add product variant
def add_product_variant(request):
    form = product_variant_form
    if request.method == 'POST':

        form = product_variant_form(request.POST, request.FILES)
        print(form)
        if not form.is_valid():
            return render(request, 'admin_partition/addfield.html',
                          {'form': form})
        product = form.save()
        print(product)
        return redirect('product:add_product_variant')
    return render(request, 'admin_partition/addfield.html', {'form': form})


# ^ Delete product
def delete_product(request, slug):
    try:
        product = Product_Variant.objects.get(product_variant_slug=slug)
    except Exception:
        return redirect('product:product_list')
    product.delete()
    messages.error(request, "product Deleted ❌")
    return redirect('product:product_list')
# soft delete


# ^ Edit product
def edit_product(request, slug):
    products = Product_Variant.objects.get(product_variant_slug=slug)
    if request.method == 'POST':
        form = product_variant_form(
            request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'admin_partition/addfield.html',
                          {'form': form})
    form = product_variant_form(instance=products)

    return render(request, 'admin_partition/addfield.html', {'form': form})
