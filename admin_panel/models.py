from django.db import models

# Create your models here.

class Product(models.Model):

    product_name        = models.CharField(max_length=50)
    description         = models.CharField(max_length=500)
    manufacture_date    = models.DateField(auto_now=False, auto_now_add=False)
    category            = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    

class Category(models.Model):

    category_name       = models.CharField(max_length=50)
    slung               = models.SlugField(unique=False)
    