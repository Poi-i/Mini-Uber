# Generated by Django 3.2.11 on 2022-01-10 01:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220109_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='create date'),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=20, unique=True, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(default='', max_length=20, verbose_name='password2'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='phone'),
        ),
    ]
