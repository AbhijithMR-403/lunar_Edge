from django.contrib import admin

from .models import Brand, Attribute, Attribute_Value
from .models import Product, Product_Variant

# Register your models here.

admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(Attribute_Value)
admin.site.register(Product_Variant)
admin.site.register(Product)
