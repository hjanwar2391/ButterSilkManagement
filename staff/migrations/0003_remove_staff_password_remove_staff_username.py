# Generated by Django 5.0.6 on 2024-05-30 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_alter_attendance_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='password',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='username',
        ),
    ]