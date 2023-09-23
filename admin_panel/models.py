from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    category_name       = models.CharField(max_length=20, unique=True)
    slug                = models.SlugField(max_length=20,unique=False)
    description         = models.TextField(max_length=2000,blank= True)
    parent              = models.ForeignKey("Category", on_delete=models.CASCADE,null=True,blank=True)
    is_available        = models.BooleanField(default=True)
    soft_deleted        = models.BooleanField(default=False)
    category_img        = models.ImageField(upload_to='photos/categories',null=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    product_name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=500,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200,blank=True)
    description = models.TextField(max_length=2000, blank=True)
    price = models.IntegerField()
    offer_price = models.IntegerField(blank=True)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    product_images = models.ImageField(upload_to='photos/products',null=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
           return self.product_name