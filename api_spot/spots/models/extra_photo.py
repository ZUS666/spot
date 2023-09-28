from django.db import models

from spots.models.location import Location


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
    description = models.CharField(
        'Описание',
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ('location',)

    def __str__(self) -> str:
        return self.location.name
