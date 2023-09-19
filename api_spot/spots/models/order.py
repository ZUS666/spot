from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

from spots.models.spot import Spot
import spots.constants as constants

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
        verbose_name='Автор',
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
    time = MultiSelectField(
        choices=constants.TIME_CHOICES,
        max_length=constants.MAX_LENGTH_CHOICES
    )
    bill = models.IntegerField('итоговый счет')

    def validate_unique(self, *args, **kwargs):
        super(Order, self).validate_unique(*args, **kwargs)
        qs = self.__class__._default_manager.filter(
            spot=self.spot,
            date=self.date,
        ).values_list('time', flat=True)
        for time in qs:
            intersection = set(time).intersection(self.time)
            if intersection:
                raise ValidationError({
                    NON_FIELD_ERRORS: 'Данный коворкинг ужe'
                                      'забронирован на это время'
                })

    class Meta:
        """Класс Meta для Order описание метаданных."""
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f'{self.user} {self.spot}'
