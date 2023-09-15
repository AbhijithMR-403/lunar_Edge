from django.db import models

# Create your models here.

class Category(models.Model):

    category_name       = models.CharField(max_length=50)
    slung               = models.SlugField(unique=True)



class Product(models.Model):

    product_name        = models.CharField(max_length=50)
    description         = models.CharField(max_length=500)
    manufacture_date    = models.DateField(auto_now=False, auto_now_add=False)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    