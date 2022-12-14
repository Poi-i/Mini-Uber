# Generated by Django 4.0.1 on 2022-01-17 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_driver_car_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=100, unique=True, verbose_name='email'),
        ),
    ]
