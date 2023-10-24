from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import spots.constants as constants
from spots.models.order import Order


User = get_user_model()


class Review(models.Model):
    """Класс для отзывов"""
    booked_spot = models.OneToOneField(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='reviews',
        error_messages={
            'unique': 'Отзыв у этого Заказа уже существует.'
        }
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
        max_length=constants.MAX_LENGTH_DESC_REVIEW
    )
    pub_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def clean(self) -> None:
        if self.booked_spot.status != constants.FINISH:
            msg = 'Нельзя оставлять отзывы на не завершенный заказ.'
            raise ValidationError({
                'booked_spot': msg
            })
        return super().clean()

    class Meta:
        """Класс меты для Review"""
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return f'Отзыв {self.pk}'
