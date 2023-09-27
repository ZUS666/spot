import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models
from multiselectfield import MultiSelectField

import spots.constants as constants
from spots.models.spot import Spot
from spots.validators import check_date_time

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
        choices=constants.START_CHOICES,
        default=constants.START_CHOICES[0][0],
    )
    end_time = models.TimeField(
        verbose_name='Время конца брони',
        choices=constants.END_CHOICES,
        default=constants.END_CHOICES[0][0],
    )
    time = MultiSelectField(
        choices=constants.TIME_CHOICES,
        max_length=100,
        blank=True,
        null=True,
    )
    bill = models.DecimalField(
        'Итоговый чек',
        max_digits=10,
        blank=True,
        null=True,
        decimal_places=2,
    )

    def get_bill(self):
        """Получнения итогово счета."""
        start = datetime.datetime.strptime(
            f'{self.date} {self.start_time}', '%Y-%m-%d %H:%M:%S'
        )
        end = datetime.datetime.strptime(
            f'{self.date} {self.end_time}', '%Y-%m-%d %H:%M:%S'
        )
        timedelta = Decimal(
            (end - start).total_seconds() / constants.SECONDS_IN_HOUR
        )
        self.bill = self.spot.price.total_price * timedelta
        return self.bill

    @property
    def date_finish(self):
        """Свойство , возращает datetime конца брони."""
        return datetime.datetime.strptime(
            f'{self.date} {self.end_time}', '%Y-%m-%d %H:%M:%S'
        )

    def validate_unique(self, *args, **kwargs):
        super(Order, self).validate_unique(*args, **kwargs)
        # Валидация по полю time
        # qs = self.__class__._default_manager.filter(
        #     spot=self.spot,
        #     date=self.date,
        # ).exclude(pk=self.pk).values_list('time', flat=True)
        # for time in qs:
        #     intersection = set(time).intersection(self.time)
        #     if intersection:
        #         raise ValidationError({
        #             NON_FIELD_ERRORS: 'Данный коворкинг ужe'
        #                               'забронирован на это время'
        #                               'TIME мульти'
        #         })

        # валидация по start и end
        qs = self.__class__._default_manager.filter(
            spot=self.spot,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({
                NON_FIELD_ERRORS: 'Данный коворкинг уже забронирован',
            })

    def clean(self):
        check_date_time(self)
        return super().clean()

    def save(self, *args, **kwargs):
        self.get_bill()
        return super().save(*args, **kwargs)

    class Meta:
        """Класс Meta для Order описание метаданных."""
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('date', 'start_time')

    def __str__(self) -> str:
        return f'Локация = {self.spot.location} , спот = {self.spot}'
