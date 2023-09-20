from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Favorite(models.Model):
    """Класс избранного"""
    user = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    location = models.ForeignKey(
        'spots.Location',
        verbose_name='Коворкинг',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        """Класс Meta для Favorite описание метаданных."""
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'location'),
                name='unique_user_location_favorite'
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} {self.location}'
