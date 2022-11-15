from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    # user_name = forms.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'phone_no', 'address', 'province', 'district',
                  'city']

