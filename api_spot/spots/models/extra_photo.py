from django.db import models


class Image(models.Model):
    location = models.ForeignKey(
        'spots.Location',
        related_name='location_image',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        blank=False,
        upload_to='images/',
        verbose_name='Фото',
        help_text='Фото места',
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
