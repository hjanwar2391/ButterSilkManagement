# Generated by Django 5.0.6 on 2024-06-04 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_management', '0004_dailysales_return_product_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='depositamount',
            old_name='Store',
            new_name='store',
        ),
    ]