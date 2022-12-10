# Generated by Django 4.1.2 on 2022-12-05 08:06

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('phone_no', models.IntegerField(blank=True, default=None, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'male'), ('F', 'female')], default=None, max_length=20, null=True)),
                ('province', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('district', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MeetUps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('full_name', models.CharField(blank=True, max_length=30)),
                ('not_editable_age', models.IntegerField(default=18, editable=False)),
                ('editable_age', models.IntegerField()),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=30)),
                ('pant_size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=30)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('now_date', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='uploads/')),
                ('upload', models.FileField(upload_to='uploads/')),
                ('time_now', models.TimeField()),
                ('date_now', models.DateTimeField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=16)),
                ('total_price', models.IntegerField()),
                ('status', models.CharField(choices=[('A', 'active'), ('I', 'inactive'), ('C', 'canceled')], default='A', max_length=30)),
                ('shipping_address', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
                ('price', models.IntegerField()),
                ('in_stock', models.IntegerField()),
                ('photo', models.ImageField(upload_to='cars')),
                ('specs', models.FileField(upload_to='specs')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='abpractice.category')),
            ],
        ),
        migrations.CreateModel(
            name='Placed_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=300)),
                ('product_photo', models.ImageField(upload_to='cars')),
                ('product_description', models.CharField(max_length=300)),
                ('product_price', models.IntegerField()),
                ('product_specs', models.FileField(upload_to='specs')),
                ('product_category', models.CharField(max_length=300)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='abpractice.order')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abpractice.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
