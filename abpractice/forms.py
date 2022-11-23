from django import forms
from .models import CustomUser, Product ,Category, Cart

class UserForm(forms.ModelForm):
    # user_name = forms.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields = '__all__'
        # fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'gender', 'phone_no', 'address', 'province', 'district',
        #           'city']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'
