from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from spots.constants import (
    LAT_MAX,
    LAT_MIN,
    LAT_MSG_ERROR,
    LONG_MAX,
    LONG_MIN,
    LONG_MSG_ERROR,
)


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
                limit_value=LAT_MIN,
                message=LAT_MSG_ERROR,
            ),
            MaxValueValidator(
                limit_value=LAT_MAX,
                message=LAT_MSG_ERROR,
            ),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Долгота',
        validators=[
            MinValueValidator(
                limit_value=LONG_MIN,
                message=LONG_MSG_ERROR,
            ),
            MaxValueValidator(
                limit_value=LONG_MAX,
                message=LONG_MSG_ERROR,
            ),
        ],
    )
    images = models.ManyToManyField(
        'spots.Image',
        related_name='locations',
        verbose_name='Изображения',
        blank=True,
    )
    plan_photo = models.ImageField(
        upload_to='images/plans/',
        verbose_name='План',
        help_text='План коворкинга',
        blank=True,
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        apart = self.apartment_number
        return (
            f'{self.street}, {self.house_number}{", "+apart if apart else ""}'
        )
