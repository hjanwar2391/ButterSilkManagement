# Generated by Django 5.0.6 on 2024-06-04 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_management', '0005_rename_store_depositamount_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysales',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store_management.product'),
        ),
    ]