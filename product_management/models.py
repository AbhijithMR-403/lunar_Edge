from django.db import models
from django.utils.text import slugify
from category_management.models import Category
from django.db.models import UniqueConstraint, Q


class Brand(models.Model):
    brand_name = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.attribute_name


# Attribute Value - RED,BLUE, 4GB, 8GB, 128GB , SSD , HDD
class Attribute_Value(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.attribute_value} {self.attribute.attribute_name}"


class Product(models.Model):
    product_name = models.CharField(max_length=49)
    product_catg = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    product_brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True)
    product_slug = models.SlugField(
        unique=True, blank=True, max_length=200)
    product_description = models.TextField(max_length=2500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        product_slug_name = '-'.join([
            self.product_brand.brand_name,
            self.product_name,
            self.product_catg.category_name
        ])
        base_slug = slugify(product_slug_name)
        self.product_slug = base_slug
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_brand.brand_name}-{self.product_name}"


class Product_Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    model_id = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    attributes = models.ManyToManyField(
        Attribute_Value,
        related_name='attributes')
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    product_variant_slug = models.SlugField(unique=True,
                                            blank=True,
                                            max_length=200
                                            )
    thumbnail_image = models.ImageField(upload_to='products/thumbnail')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        product_variant_slug_name = '-'.join([
            self.product.product_brand.brand_name,
            self.product.product_name,
            self.product.product_catg.category_name,
            self.model_id
        ])
        base_slug = slugify(product_variant_slug_name)
        self.product_variant_slug = base_slug
        super(Product_Variant, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                name='Unique skuid must be provided',
                fields=['product', 'model_id'],
                condition=Q(model_id__isnull=False),
            )
        ]

    def __str__(self) -> str:
        return self.product_variant_slug
