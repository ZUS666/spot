# Generated by Django 4.2.5 on 2023-10-31 22:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0014_alter_order_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='discount',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=70, message='Скидка не может превышать 70%%')], verbose_name='Скидка'),
        ),
    ]
