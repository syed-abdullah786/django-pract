# Generated by Django 4.1.2 on 2022-11-23 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abpractice', '0010_order_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='size',
            new_name='status',
        ),
    ]
