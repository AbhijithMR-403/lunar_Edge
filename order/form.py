from django import forms
from authenticator.models import AddressBook


class attribute_value_form(forms.ModelForm):
    class Meta:
        model = AddressBook
        fields = '__all__'
