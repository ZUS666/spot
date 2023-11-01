from django.contrib.auth import get_user_model
from django.db import models, transaction
from django_celery_beat.models import PeriodicTask

from promo.constants import MAX_PROMO_DISCOUNT
from promo.validators import (
    MaxDiscountValidator, validate_date_less_present,
    validate_datetime_less_present,
)
from spots.constants import CATEGORY_CHOICES


User = get_user_model()


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
        validators=(validate_date_less_present,),
    )
    balance = models.PositiveIntegerField(
        'Количество использований',
    )
    only_category = models.CharField(
        'Только для категории',
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
    )
    one_off = models.BooleanField(
        'Однократное использование пользователем',
        default=True,
    )
    used_user = models.ManyToManyField(
        User,
        related_name='promocode',
        verbose_name='Оборудование',
        through='PromocodeUser',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ('expiry_date',)


class PromocodeUser(models.Model):
    user = models.ForeignKey(
        User,
        related_name='promocode_user',
        on_delete=models.CASCADE,
    )
    promocode = models.ForeignKey(
        Promocode,
        related_name='promocode_user',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Пользователь-промокод'
        verbose_name_plural = 'Пользователи-промокоды'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'promocode'),
                name='unique_user_promocode',
            ),
        )


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
    promocode = models.ForeignKey(
        Promocode,
        related_name='promocodes',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_sent = models.BooleanField(
        'Отправлен',
        default=False,
    )
    task = models.OneToOneField(
        PeriodicTask,
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

    @transaction.atomic
    def save(self, *args, **kwargs):
        from promo.services import create_task_after_save_promo_email
        if self.task:
            self.task.delete()
        self.is_sent = False
        self.task = create_task_after_save_promo_email(self)
        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.task:
            self.task.delete()
        super().delete(*args, **kwargs)
