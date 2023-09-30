from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from category_management.models import *
from product_management.models import *
from .models import *
from django.contrib import messages
import uuid



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




def profile(request):
   
   context={
      'user_details':Account.objects.get(email=request.user)
   }
   return render(request,'user_partition/user_page/profile.html',context)


#to get the cart id if present
def _cart_id(request):
    if not request.session['cart']:
       request.session['cart']=uuid.uuid4
    return request.session.session_key or request.session['cart']

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



def checkout(request):
   # print(Cart.cart_id.values(),request.session.session_key)
   cart_id=Cart.objects.get(cart_id=request.session.session_key)
   cart_details = Cart_item.objects.select_related('cart_id').filter(cart_id=cart_id)
   context ={
       'cart_details':cart_details
    }
   return render(request,'user_partition/user_page/checkout.html',context)