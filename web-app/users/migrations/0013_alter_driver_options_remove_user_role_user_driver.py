# Generated by Django 4.0.1 on 2022-01-17 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_driver_id_remove_ride_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='driver',
            options={'verbose_name': 'Driver'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='driver',
            field=models.BooleanField(default=False, editable=False, verbose_name='if this user is a driver'),
        ),
    ]
