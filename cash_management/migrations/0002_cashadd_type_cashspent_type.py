# Generated by Django 5.0.6 on 2024-05-31 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashadd',
            name='type',
            field=models.CharField(default='Added', max_length=10),
        ),
        migrations.AddField(
            model_name='cashspent',
            name='type',
            field=models.CharField(default='Spent', max_length=10),
        ),
    ]
