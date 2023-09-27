from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from spots.constants import (MAX_DISCOUNT, MAX_DISCOUNT_MESSAGE, MIN_VALUE,
                             PRICE_NEGATIVE_OR_ZERO_MESSAGE)


class Price(models.Model):
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=(
            MinValueValidator(
                limit_value=MIN_VALUE,
                message=PRICE_NEGATIVE_OR_ZERO_MESSAGE,
            ),
        ),
    )
    discount = models.PositiveSmallIntegerField(
        'Скидка',
        default=0,
        validators=(
            MaxValueValidator(
                limit_value=MAX_DISCOUNT,
                message=MAX_DISCOUNT_MESSAGE,
            ),
        )
    )
    total_price = models.DecimalField(
        'Итоговая стоимость',
        max_digits=10,
        blank=True,
        null=True,
        decimal_places=2,
        validators=(
            MinValueValidator(
                limit_value=MIN_VALUE,
                message=PRICE_NEGATIVE_OR_ZERO_MESSAGE,
            ),
        ),
    )
    description = models.TextField(
        'Описание',
        max_length=500,
        blank=True,
    )

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'

    def __str__(self):
        return self.description[:20]

    def get_total_price(self):
        if self.discount:
            self.total_price = self.price - self.price * self.discount / 100
        else:
            self.total_price = self.price
        return self.total_price

    def save(self, *args, **kwargs):
        self.get_total_price()
        return super().save(*args, **kwargs)
