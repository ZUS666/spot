from django.db import models

from spots.models.location import Location
from spots.utils import prepare_image
from spots.constants import SMALL_HEIGHT, SMALL_WIDTH


class SmallMainPhoto(models.Model):
    """Модель для укороченных фотографий(для карт)."""
    location = models.OneToOneField(
        Location,
        related_name='small_main_photo',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Укороченное фото',
        upload_to='images/small_main_photo/',
    )

    def save(self, *args, **kwargs):
        """Обработка изображения после сохранения в базу данных"""
        super(SmallMainPhoto, self).save(*args, **kwargs)
        if self.image:
            prepare_image(self.image.path, SMALL_WIDTH, SMALL_HEIGHT)

    class Meta:
        verbose_name = 'Укороченное фото'
        verbose_name_plural = 'Укороченные фото'
        ordering = ('location',)

    def __str__(self) -> str:
        return self.location.name
