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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['class']=''
        
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_slug']

    #   ? example
       


class product_variant_form(forms.ModelForm):
    class Meta:
        model = Product_Variant
        fields = '__all__'
        exclude = ['is_active','product_variant_slug']

        widgets = {
            'product'        : forms.RadioSelect,
            'model_id'       : forms.TextInput(attrs={'class':"form-control"}),
            'attributes'     : forms.CheckboxSelectMultiple,
            'sale_price'     : forms.TextInput(attrs={'class':"form-control"}),
            'stock'          : forms.TextInput(attrs={'class':"form-control"}),
            'thumbnail_image': forms.ClearableFileInput,
            'max_price'      : forms.TextInput(attrs={'class':"form-control"}),
        }