from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    gender = [
        ('M', 'male'),
        ('F', 'female')]
    address = models.CharField(max_length=200, default=None, null=True, blank=True)
    phone_no = models.IntegerField(default=None, null=True, blank=True)
    gender = models.CharField(choices=gender, max_length=20, default=None, null=True, blank=True)
    province = models.CharField(max_length=200, default=None, null=True, blank=True)
    district = models.CharField(max_length=200, default=None, null=True, blank=True)
    city = models.CharField(max_length=200, default=None, null=True, blank=True)


class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    in_stock = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.category_name}'


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Order(models.Model):
    total_price = models.IntegerField()
    user = models.OneToOneField(CustomUser, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=100)



class Locations(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class MeetUps(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    PANT_SIZES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=30, blank=True)
    not_editable_age = models.IntegerField(editable=False, default=18)
    editable_age = models.IntegerField()
    size = models.CharField(choices=SHIRT_SIZES, max_length=30)
    pant_size = models.CharField(choices=PANT_SIZES, max_length=30)
    add_date = models.DateTimeField(auto_now_add=True)
    now_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='uploads/')
    upload = models.FileField(upload_to='uploads/')
    time_now = models.TimeField()
    date_now = models.DateTimeField()
    url = models.URLField()

    # location = models.OneToOneField(Locations, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
