from django.db import models
from authenticator.models import Account
from product_management.models import Product_Variant


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)


class Cart_item(models.Model):
    product_id = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
