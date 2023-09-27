from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from spots.constants import (LAT_MAX, LAT_MIN, LAT_MSG_ERROR, LONG_MAX,
                             LONG_MIN, LONG_MSG_ERROR, MEETING_ROOM,
                             NAME_CACHE_MEETING_ROOM, NAME_CACHE_WORKSPACE,
                             WORK_SPACE)
from spots.services import count_spots, get_low_price, get_rating_location


class Location(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        unique=True,
    )
    open_time = models.TimeField(
        'Время открытия',
    )
    close_time = models.TimeField(
        'время закрытия',
    )
    street = models.CharField(
        'Улица',
        max_length=100,
    )
    house_number = models.CharField(
        'Номер дома',
        max_length=10,
    )
    metro = models.CharField(
        'Метро',
        max_length=128,
        blank=True,
        null=True
    )
    city = models.CharField(
        'Город',
        max_length=64,
    )
    latitude = models.DecimalField(
        'Широта',
        max_digits=9,
        decimal_places=6,
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
        'Долгота',
        max_digits=9,
        decimal_places=6,
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
    main_photo = models.ImageField(
        'Главное фото',
        upload_to='images/main_photo/',
        help_text='Главное фото локации',
        blank=True,
    )
    plan_photo = models.ImageField(
        'План',
        upload_to='images/plans/',
        help_text='План коворкинга',
        blank=True,
    )
    description = models.TextField(
        'Описание',
        max_length=500,
        blank=True,
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def count_workspace(self, *args, **kwargs):
        """
        Получение количества рабочих мест.
        """
        return count_spots(self, WORK_SPACE, NAME_CACHE_WORKSPACE)

    def count_meeting_room(self, *args, **kwargs):
        """
        Получение количества переговорных.
        """
        return count_spots(self, MEETING_ROOM, NAME_CACHE_MEETING_ROOM)

    def rating(self, *args, **kwargs):
        return get_rating_location(self)

    def low_price(self, *args, **kwargs):
        return get_low_price(self)

    def get_full_address_str(self):
        return f'г. {self.city}, ул. {self.street}, {self.house_number}'
