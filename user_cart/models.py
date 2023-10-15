from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=128, unique=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    expiration_date = models.DateField(auto_now_add=True)
    minimum_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.code
