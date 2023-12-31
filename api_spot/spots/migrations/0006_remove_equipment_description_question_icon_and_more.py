# Generated by Django 4.2.5 on 2023-10-10 12:59

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spots', '0005_equipment_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='description',
        ),
        migrations.AddField(
            model_name='question',
            name='icon',
            field=models.FileField(default=1, upload_to='icons/question/', validators=[django.core.validators.FileExtensionValidator(('svg',))]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='icon',
            field=models.FileField(upload_to='icons/equipment/', validators=[django.core.validators.FileExtensionValidator(('svg',))]),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='spots.location', verbose_name='Локация'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_time',
            field=models.TimeField(choices=[(datetime.time(1, 0), '00:55'), (datetime.time(2, 0), '01:55'), (datetime.time(3, 0), '02:55'), (datetime.time(4, 0), '03:55'), (datetime.time(5, 0), '04:55'), (datetime.time(6, 0), '05:55'), (datetime.time(7, 0), '06:55'), (datetime.time(8, 0), '07:55'), (datetime.time(9, 0), '08:55'), (datetime.time(10, 0), '09:55'), (datetime.time(11, 0), '10:55'), (datetime.time(12, 0), '11:55'), (datetime.time(13, 0), '12:55'), (datetime.time(14, 0), '13:55'), (datetime.time(15, 0), '14:55'), (datetime.time(16, 0), '15:55'), (datetime.time(17, 0), '16:55'), (datetime.time(18, 0), '17:55'), (datetime.time(19, 0), '18:55'), (datetime.time(20, 0), '19:55'), (datetime.time(21, 0), '20:55'), (datetime.time(22, 0), '21:55'), (datetime.time(23, 0), '22:55'), (datetime.time(0, 0), '23:55')], default=datetime.time(1, 0), verbose_name='Время конца брони'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_time',
            field=models.TimeField(choices=[(datetime.time(0, 0), '00:00'), (datetime.time(1, 0), '01:00'), (datetime.time(2, 0), '02:00'), (datetime.time(3, 0), '03:00'), (datetime.time(4, 0), '04:00'), (datetime.time(5, 0), '05:00'), (datetime.time(6, 0), '06:00'), (datetime.time(7, 0), '07:00'), (datetime.time(8, 0), '08:00'), (datetime.time(9, 0), '09:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')], default=datetime.time(0, 0), verbose_name='Время начала брони'),
        ),
    ]
