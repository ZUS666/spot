from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from spots.models.order import Order

User = get_user_model()


class Review(models.Model):
    """Класс для отзывов"""
    user = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    booked_spot = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    raiting = models.PositiveSmallIntegerField(
        "Оценка отзыва",
        validators=(MinValueValidator(1), MaxValueValidator(5)),
    )
    description = models.TextField(
        "Текст отзыва",
        max_length=100
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True
    )

    class Meta:
        """Класс меты для Review"""
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.pk}"
