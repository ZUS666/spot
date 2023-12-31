# Generated by Django 4.2.5 on 2023-10-10 11:29

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_occupation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, validators=[users.validators.NamesValidator()], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, validators=[users.validators.NamesValidator()], verbose_name='Фамилия'),
        ),
    ]
