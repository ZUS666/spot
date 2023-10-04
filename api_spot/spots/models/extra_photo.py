from django.db import models

from spots.models.location import Location
from spots.utils import prepare_image


class ExtraPhoto(models.Model):
    location = models.ForeignKey(
        Location,
        related_name='location_extra_photo',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Фото',
        blank=False,
        upload_to='images/',
        help_text='Фото места',
    )

    def save(self, *args, **kwargs):
        """Обработка изображения перед сохранением в базу данных"""
        super(ExtraPhoto, self).save(*args, **kwargs)
        if self.image:
            filepath = self.image.path
            prepare_image(self.image, filepath)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ('location',)

    def __str__(self) -> str:
        return self.location.name
