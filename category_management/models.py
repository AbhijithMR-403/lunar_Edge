from django.db import models
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=False)
    description = models.TextField(max_length=200, blank=True)
    parent = models.ForeignKey('self',
                               null=True, blank=True, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    category_img = models.ImageField(upload_to='categories')
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
