from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from spots.services import count_spots
from spots.constants import (LAT_MAX, LAT_MIN, LAT_MSG_ERROR, LONG_MAX,
                             LONG_MIN, LONG_MSG_ERROR, WORK_SPACE,
                             MEETING_ROOM, NAME_CACHE_MEETING_ROOM,
                             NAME_CACHE_WORKSPACE)


class Location(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        unique=True,
    )
    open_time = models.TimeField(
        'Время открытия',
        blank=True,
        null=True
    )
    close_time = models.TimeField(
        'время закрытия',
        blank=True,
        null=True
    )
    street = models.CharField(
        'Улица',
        max_length=100,
    )
    house_number = models.CharField(
        'Номер дома',
        max_length=10,
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
        return count_spots(self, WORK_SPACE, NAME_CACHE_WORKSPACE)

    def count_meeting_room(self, *args, **kwargs):
        return count_spots(self, MEETING_ROOM, NAME_CACHE_MEETING_ROOM)
