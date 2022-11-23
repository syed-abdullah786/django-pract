from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import CustomUser, Cart, Product, Category, Order
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Product)



class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'password', 'email', 'gender', 'address', 'phone_no'
    )
    add_fieldsets = ((None, {
            'fields': ()
        }),(None,
         {'fields': ('username', 'password1', 'password2', 'email', 'address', 'phone_no', 'gender', 'province', 'district', 'city')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
