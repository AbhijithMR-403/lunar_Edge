from django import forms
from authenticator.models import AddressBook


class addressbook_form(forms.ModelForm):
    class Meta:
        model = AddressBook
        fields = '__all__'
        exclude = ['created_at', 'user',
                   'updated_at', 'is_default', 'is_active']

