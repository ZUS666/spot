# Generated by Django 4.2.5 on 2023-10-04 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0004_location_days_open_location_short_annotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extraphoto',
            name='description',
        ),
    ]
