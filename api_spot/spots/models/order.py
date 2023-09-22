import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models

import spots.constants as constants
from spots.models.spot import Spot

User = get_user_model()


class Order(models.Model):
    """Класс заказа"""
    spot = models.ForeignKey(
        Spot,
        verbose_name='Коворкинг',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=constants.MAX_LENGTH_STATUS,
        choices=constants.ORDER_STATUS_CHOICES,
        default=constants.WAIT_PAY,
    )
    date = models.DateField(
        verbose_name='Дата заказа'
    )
    start_time = models.TimeField(
        verbose_name='Время начала брони',
        choices=constants.TIME_CHOICES,
        default=constants.TIME_CHOICES[0][0],
    )
    end_time = models.TimeField(
        verbose_name='Время конца брони',
        choices=constants.TIME_CHOICES,
        default=constants.TIME_CHOICES[1][0],
    )

    @property
    def date_finish(self):
        """Свойство , возращает datetime конца брони."""
        return datetime.datetime.strptime(
            f'{self.date} {self.end_time}', '%Y-%m-%d %H:%M:%S'
        )

    def validate_unique(self, *args, **kwargs):
        super(Order, self).validate_unique(*args, **kwargs)
        if not (
            isinstance(self.start_time, datetime.time)
            and isinstance(self.end_time, datetime.time)
        ):
            raise ValidationError("")
        qs = self.__class__._default_manager.filter(
            spot=self.spot,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if qs.exists():
            raise ValidationError({
                NON_FIELD_ERRORS: 'Данный коворкинг уже забронирован',
            })

    def clean(self):
        print(self.start_time)
        date_time_now = datetime.datetime.strptime(
            f'{self.date} {self.start_time}', '%Y-%m-%d %H:%M:%S'
        )
        if date_time_now < datetime.datetime.now():
            raise ValidationError({
                'start_time': 'Нельзя забронировать в прошлом.'
            })
        if self.end_time == self.start_time:
            raise ValidationError({
                'end_time': 'Конец брони не может совпадать с началом'
            })
        if self.end_time < self.start_time:
            raise ValidationError({
                'end_time': 'Конец брони должен быть позже начала'
            })
        return super().clean()

    class Meta:
        """Класс Meta для Order описание метаданных."""
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('date', 'start_time')

    def __str__(self) -> str:
        return f'{self.spot.location} {self.spot} {self.user}'
