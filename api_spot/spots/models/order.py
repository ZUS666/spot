from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.models import Q, F

from spots.models.spot import Spot

User = get_user_model()


BOOKED = "Booked"
LOCK = "Lock"
ORDER_STATUS_CHOICES = [
    (BOOKED, "Booked"),
    (LOCK, "Lock")
]


class Order(models.Model):
    """Класс заказа"""
    spot = models.ForeignKey(
        Spot,
        verbose_name="Коворкинг",
        on_delete=models.CASCADE,
        related_name="orders"
    )
    user = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="orders"
    )
    status = models.TextField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default=BOOKED,
    )
    start_date = models.DateTimeField(
        verbose_name="Начало брони",
    )
    end_date = models.DateTimeField(
        verbose_name="Конец брони",
    )
    bill = models.TextField()

    def validate_unique(self, *args, **kwargs):
        super(Order, self).validate_unique(*args, **kwargs)
        if not (
            isinstance(self.start_date, datetime)
            and isinstance(self.end_date, datetime)
        ):
            raise ValidationError("")
        qs = self.__class__._default_manager.filter(
            spot=self.spot,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        )
        if qs.exists():
            raise ValidationError({
                NON_FIELD_ERRORS: ['Данный коворкинг уже забронирован', ],
            })

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('Start should be before end')
        return super().clean()

    class Meta:
        """Класс Meta для Order описание метаданных."""
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('start_date',)
        constraints = [
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date')),
                name='start_before_end'
            ),
        ]

    def __str__(self) -> str:
        return f'{self.user} {self.spot}'
