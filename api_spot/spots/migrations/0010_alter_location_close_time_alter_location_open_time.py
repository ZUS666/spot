# Generated by Django 4.2.5 on 2023-10-15 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("spots", "0009_delete_event_delete_question_delete_rule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="close_time",
            field=models.TimeField(
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
                    ("20:00", "20:00"),
                    ("21:00", "21:00"),
                    ("22:00", "22:00"),
                ],
                default="08:00",
                verbose_name="время закрытия",
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="open_time",
            field=models.TimeField(
                choices=[
                    ("07:00", "07:00"),
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
                    ("20:00", "20:00"),
                    ("21:00", "21:00"),
                ],
                default="07:00",
                verbose_name="Время открытия",
            ),
        ),
    ]
