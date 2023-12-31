from django.db import models
from authenticator.models import Account
from product_management.models import Product_Variant
from user_cart.models import Coupon


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)
    created_date = models.DateField(auto_now_add=True)
    subtotal = models.IntegerField(default=0, null=True)


class Cart_item(models.Model):
    product_id = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    title = models.CharField(max_length=256)
