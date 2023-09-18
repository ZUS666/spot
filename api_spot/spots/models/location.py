from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Image(models.Model):
    location = models.ForeignKey(
        'Location',
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


class Location(models.Model):
    street = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Улица',
    )
    house_number = models.CharField(
        max_length=10,
        blank=False,
        verbose_name='Номер дома',
    )
    apartment_number = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Номер квартиры',
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Широта',
        validators=[
            MinValueValidator(
                limit_value=settings.LAT_MIN,
                message=settings.LAT_MSG_ERROR,
            ),
            MaxValueValidator(
                limit_value=settings.LAT_MAX,
                message=settings.LAT_MSG_ERROR,
            ),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Долгота',
        validators=[
            MinValueValidator(
                limit_value=settings.LONG_MIN,
                message=settings.LONG_MSG_ERROR,
            ),
            MaxValueValidator(
                limit_value=settings.LONG_MAX,
                message=settings.LONG_MSG_ERROR,
            ),
        ],
    )
    images = models.ManyToManyField(
        Image,
        related_name='locations',
        verbose_name='Изображения',
        blank=True,
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        apart = self.apartment_number
        return (
            f'{self.street}, {self.house_number}{", "+apart if apart else ""}'
        )
