from django.db import models
from django.contrib.auth import get_user_model

from spots.models.location import Location

User = get_user_model()


class Favorite(models.Model):
    """Класс избранного"""
    user = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    location = models.ForeignKey(
        Location,
        verbose_name="Коворкинг",
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True
    )

    class Meta:
        """Класс Meta для Favorite описание метаданных."""
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=("user", "location"),
                name="unique_user_location_favorite"
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} {self.location}'
