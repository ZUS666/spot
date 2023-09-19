# Generated by Django 4.2.5 on 2023-09-19 11:02

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):
    dependencies = [
        ("spots", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="time",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("08:00", "08:00"),
                    ("09:00", "09:00"),
                    ("10:00", "10:00"),
                    ("11:00", "11:00"),
                    ("12:00", "12:00"),
                    ("13:00", "13:00"),
                    ("14:00", "14:00"),
                    ("15:00", "15:00"),
                    ("16:00", "16:00"),
                    ("17:00", "17:00"),
                    ("18:00", "18:00"),
                    ("19:00", "19:00"),
                ],
                max_length=9,
            ),
        ),
    ]
