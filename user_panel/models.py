from django.db import models
from authenticator.models import *
from product_management.models import *


# Create your models here.

class Cart(models.Model):
    cart_id         = models.CharField(blank=True)
    total_price     = models.IntegerField(default=0)
    created_date    = models.DateField(auto_now_add=True)
    
class Cart_item(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product_id = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)