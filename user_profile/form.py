from django import forms
from authenticator.models import user_profile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = user_profile
        fields = ['profile_img']
