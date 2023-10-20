from django.db import models

from spots.constants import SMALL_HEIGHT, SMALL_WIDTH
from spots.models.location import Location
from spots.services import image_resize


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
        image_resize(self.image, SMALL_WIDTH, SMALL_HEIGHT)
        super(SmallMainPhoto, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Укороченное фото'
        verbose_name_plural = 'Укороченные фото'
        ordering = ('location',)

    def __str__(self) -> str:
        return self.location.name
