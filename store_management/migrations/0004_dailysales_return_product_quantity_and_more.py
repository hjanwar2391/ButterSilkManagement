# Generated by Django 5.0.6 on 2024-06-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_management', '0003_dailysales_store_depositamount_store_product_store_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysales',
            name='return_product_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailysales',
            name='sell_due',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
