from django.db import models

from promo.constants import MAX_PROMO_DISCOUNT
from promo.validators import (
    MaxDiscountValidator, validate_datetime_less_present,
)
from promo.services import create_task_after_save_promo_email


class Promocode(models.Model):
    name = models.CharField(
        'Название промокода',
        max_length=64,
        unique=True,
    )
    percent_discount = models.PositiveSmallIntegerField(
        'Процент скидки',
        validators=(MaxDiscountValidator(MAX_PROMO_DISCOUNT),)
    )
    expiry_date = models.DateField(
        'Дата истечения',
        validators=(validate_datetime_less_present,),
    )
    balance = models.PositiveIntegerField(
        'Количество использований',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ('expiry_date',)


class EmailNews(models.Model):
    subject_message = models.CharField(
        'Тема письма',
        max_length=128
    )
    text_message = models.TextField(
        'Текст письма'
    )
    send_datetime = models.DateTimeField(
        'Дата и время отправки',
        validators=(validate_datetime_less_present,),
        unique=True,
    )
    promo_code = models.ForeignKey(
        Promocode,
        related_name='promocode',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.subject_message[:20]

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        ordering = ('send_datetime',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        create_task_after_save_promo_email(self)
