from django import forms
from .models import Product


class product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','category','brand','description', 'price','offer_price','quantity','is_available','soft_deleted','product_images',)