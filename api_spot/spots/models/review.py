from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import spots.constants as constants
from spots.models.order import Order

User = get_user_model()


class Review(models.Model):
    """Класс для отзывов"""
    user = models.ForeignKey(
        User,
        blank=True, null=True,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        related_name='reviews'
    )
    booked_spot = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        'Оценка отзыва',
        validators=(
            MinValueValidator(constants.MIN_EVALUATION),
            MaxValueValidator(constants.MAX_EVALUATION)
        ),
    )
    description = models.TextField(
        'Текст отзыва',
        max_length=constants.MAX_LENGTH_DESC
    )
    pub_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        """Класс меты для Review"""
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв {self.pk}'
