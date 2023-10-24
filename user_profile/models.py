from django.db import models
from authenticator.models import Account
from product_management.models import Product_Variant
# # Create your models here.


class WishList(models.Model):
    product = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
