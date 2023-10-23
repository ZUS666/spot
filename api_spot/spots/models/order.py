import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

import spots.constants as constants
from spots.models.spot import Spot
from spots.validators import check_date_time, check_spot_order


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
    bill = models.DecimalField(
        'Итоговый чек',
        max_digits=10,
        blank=True,
        null=True,
        decimal_places=2,
    )

    def get_bill(self) -> Decimal:
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
    def date_finish(self) -> datetime:
        """Свойство , возращает datetime конца брони."""
        return datetime.datetime.strptime(
            f'{self.date} {self.end_time}', '%Y-%m-%d %H:%M:%S'
        )

    def validate_unique(self, *args, **kwargs):
        super(Order, self).validate_unique(*args, **kwargs)
        check_spot_order(self)

    def clean(self) -> None:
        check_date_time(
            self.date,
            self.start_time,
            self.end_time,
            self.spot.location,
        )
        return super().clean()

    def save(self, *args, **kwargs) -> None:
        from django.db import transaction
        from ..tasks import change_status_task

        self.get_bill()
        if not self.pk:
            super().save(*args, **kwargs)
            transaction.on_commit(lambda: change_status_task.apply_async(
                args=[self.pk], countdown=settings.TIME_CHANGE_STATUS
            ))
        else:
            super().save(*args, **kwargs)

    class Meta:
        """Класс Meta для Order описание метаданных."""
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('date', 'start_time')

    def __str__(self) -> str:
        return f'Локация id = {self.spot.location.id}, спот={self.spot.id}'
