# Generated by Django 4.2.5 on 2023-09-20 20:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("spots", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="spot",
            name="number",
            field=models.IntegerField(default=1, verbose_name="Номер комнаты"),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="spot",
            constraint=models.UniqueConstraint(
                fields=("category", "number"), name="unique_category_number_spot"
            ),
        ),
    ]
