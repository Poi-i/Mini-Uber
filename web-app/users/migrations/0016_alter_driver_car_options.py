# Generated by Django 4.0.1 on 2022-01-17 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_rename_driver_driver_car'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='driver_car',
            options={'verbose_name': 'Driver_Car'},
        ),
    ]
