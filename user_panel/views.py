from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from category_management.models import *
from product_management.models import *
from .models import *
from django.contrib import messages
# Create your views here.

def home_page(request):
   content = {
      'products':Product_Variant.objects.all(),
      'categories':Category.objects.all(),
      }
   return render(request,'user_partition/user_page/home.html',content)

def product_page(request):
   content ={
      'products' : Product_Variant.objects.all()
   }
   return render(request,'user_partition/user_page/shop.html',content)

def logout_user(request):
   logout(request)
   return redirect('user_home:home')

def product_details(request,id):
   detail=Product_Variant.objects.get(id=id)
   return render(request,'user_partition/user_page/product_detail.html',{'detail':detail})


# def user_cart(request):
#    cart_id=Cart.objects.get(session_id=request.session.session_key).id
#    cart_list=Cart_item.objects.select_related('cart_id').filter(cart_id=cart_id)
#    for cart_item in cart_list:
#       print('hello', cart_item.product_id)

#    content={
#    'cart_items':cart_list
#    }
#    return render(request,'user_partition/user_page/cart.html',content)


# def add_to_cart(request,slug):
#    # ^ Checking for session key
#    session_key=request.session.session_key
#    if session_key is None:
#       messages.warning(request,'Login Before Adding To Cart')
#       return redirect('user_partition:userlogin')
   
#    cart_object = Cart.objects.get_or_create(session_id=session_key)
#    product_object = Product_Variant.objects.get(product_variant_slug=slug)
#    add_cart_item = Cart_item.objects.get_or_create(
#       cart_id=cart_object[0],
#       product_id=product_object,
#       )
#    # if add_cart_item[1]:
#    #    add_cart_item[0].quantity=0
#    add_cart_item[0].quantity+=1
#    add_cart_item[0].save()
#    cart_object[0].total_price=product_object.sale_price
#    print('\n\n\n',product_object,'\n\n\n')
#    return redirect('user_home:user_cart')

def profile(request):
   context={
      'user_details':Account.objects.get(email=request.user)
   }
   return render(request,'user_partition/user_page/profile.html',context)


#to get the cart id if present
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def user_cart(request,total=0,quantity=0,cart_items=None):
    total_with_orginal_price =0
    try:
        if request.user.is_authenticated:
            cart_items = Cart_item.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_item.objects.filter(cart=cart,is_active=True)
    except:
        pass

    context = {
      #   'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
      #   'total_with_orginal_price':total_with_orginal_price
    }
    return render(request,'user_partition/user_page/cart.html',context)



# ! haven't finished


def add_to_cart(request,id):
    
    current_user = request.user
    product = Product_Variant.objects.get(id=id)    #get the product
    #if user authenticated
    cart,check = Cart.objects.get_or_create(cart_id=_cart_id(request))      
    if current_user.is_authenticated:
      try:
         cart_item = Cart_item.objects.get(product_id=product , user=current_user)
         cart_item.quantity +=1
         cart_item.save()
      except Cart_item.DoesNotExist:
         cart_item = Cart_item.objects.create(
               product_id=product,
               user=current_user,
               cart_id=cart,
               quantity = 1,
         )
         cart_item.save()
      return redirect('user_home:user_cart')
        
    else:
        
    # ===CART CREATED ===
      # cart = Cart.objects.get_or_create(cart_id=_cart_id(request))

      
      # ===Product saved to cart item
      try:
         cart_item = Cart_item.objects.get(product=product , cart=cart)
         cart_item.quantity +=1
         cart_item.save()
      except Cart_item.DoesNotExist:
         cart_item = Cart_item.objects.create(
               product=product,
               cart=cart,
               quantity = 1,
         )
         cart_item.save()
      return redirect('user_home:user_cart')
