from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

# from spots.models import Spot


class Price(models.Model):
    # TODO
    # spot = models.ForeignKey(
    #     Spot,
    #     on_delete=models.CASCADE,
    #     related_name='prices',
    #     verbose_name='Место',
    # )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        verbose_name='Цена',
        validators=[
            MinValueValidator(
                limit_value=settings.MIN_VALUE,
                message='Цена не может быть меньше или равна нулю.',
            )
        ],
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        verbose_name='Скидка',
        validators=[
            MinValueValidator(
                limit_value=settings.ZERO,
                message='Скидка не может быть меньше нуля.',
            )
        ],
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'

    def __str__(self):
        return str(self.price)
