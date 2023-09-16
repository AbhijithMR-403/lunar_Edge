from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20,unique=False)
    description = models.TextField(max_length=100,blank= True)
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    category_image = models.ImageField(upload_to='photos/categories',null=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def _str_(self):
        return self.category_name
    

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200,blank=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    offer_price = models.IntegerField(default=0)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    product_images = models.ImageField(upload_to='photos/products')

    def _str_(self):
           return self.product_name