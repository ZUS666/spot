# Generated by Django 4.2.5 on 2023-10-31 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promo', '0004_alter_promocode_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='one_off',
            field=models.BooleanField(default=True, verbose_name='Однократное использование пользователем'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='only_category',
            field=models.CharField(blank=True, choices=[('Рабочее место', 'Рабочее место'), ('Переговорная', 'Переговорная')], null=True, verbose_name='Только для категории'),
        ),
        migrations.CreateModel(
            name='PromocodeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promocode_user', to='promo.promocode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promocode_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользователь-промокод',
                'verbose_name_plural': 'Пользователи-промокоды',
            },
        ),
        migrations.AddField(
            model_name='promocode',
            name='used_user',
            field=models.ManyToManyField(related_name='promocode', through='promo.PromocodeUser', to=settings.AUTH_USER_MODEL, verbose_name='Оборудование'),
        ),
        migrations.AddConstraint(
            model_name='promocodeuser',
            constraint=models.UniqueConstraint(fields=('user', 'promocode'), name='unique_user_promocode'),
        ),
    ]
