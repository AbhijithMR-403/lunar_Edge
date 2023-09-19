from django import forms
from .models import Product


class product_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['is_available'].widget.attrs['class'] = ''
        self.fields['soft_deleted'].widget.attrs['class'] = ''
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['product_images'].widget.attrs['class'] = ''
    class Meta:
        model = Product
        fields = ('product_name','category','brand','description', 'price','offer_price','quantity','is_available','soft_deleted','product_images',)
       
       
        # widgets = {
        #     'product_name'      : forms.TextInput(attrs={'class':"form-control"}),
        #     'category'          : forms.TextInput(attrs={'class':"form-control"}),
        #     'brand'             : forms.TextInput(attrs={'class':"form-control"}),
        #     'description'       : forms.TextInput(attrs={'class':"form-control"}),
        #     'price'             : forms.TextInput(attrs={'class':"form-control"}),
        #     'offer_price'       : forms.TextInput(attrs={'class':"form-control"}),
        #     'quantity'          : forms.TextInput(attrs={'class':"form-control"}),
        #     'is_available'      : forms.TextInput(attrs={'class':"form-control"}),
        #     'soft_deleted'      : forms.TextInput(attrs={'class':"form-control"}),
        #     'product_images'    : forms.TextInput(attrs={'class':"form-control"}),
        # }