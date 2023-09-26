from django import forms
from .models import *

#  ^ Add brand
class brand_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.fields['brand_name'].widget.attrs['class'] = ''
        self.fields['is_active'].widget.attrs['class'] = ''
    class Meta:
        model = Brand
        fields = '__all__'

# ^ Add Attribute name
class attribute_name_form(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = '__all__'

# ^ Add attribute value
class attribute_value_form(forms.ModelForm):
    
    class Meta:
        model = Attribute_Value
        fields = '__all__'




class product_form(forms.ModelForm):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
       
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
        
    #     self.fields['is_available'].widget.attrs['class'] = ''
    #     self.fields['soft_deleted'].widget.attrs['class'] = ''
    #     self.fields['category'].widget.attrs['class'] = 'form-select'
    #     self.fields['product_images'].widget.attrs['class'] = ''
    # class Meta:
    #     model = Product
    #     fields = ('product_name','category','brand','description', 'price','offer_price','quantity','is_available','soft_deleted','product_images',)
       

    #   ? example
       
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