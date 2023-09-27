from django.core.cache import cache
from django.db import models

from ..constants import (
    CATEGORY_CHOICES, NAME_CACHE_LOW_PRICE,
    NAME_CACHE_MEETING_ROOM, NAME_CACHE_WORKSPACE
)
from .equipment import Equipment
from .location import Location
from .price import Price


class Spot(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название рабочего места'
    )
    price = models.ForeignKey(
        Price,
        on_delete=models.RESTRICT,
        related_name='spots',
        verbose_name='Цена',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='spots',
        verbose_name='Локация',
    )
    category = models.CharField(
        max_length=64,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория',
    )
    equipment = models.ManyToManyField(
        Equipment,
        related_name='spots',
        verbose_name='Оборудование',
        through='SpotEquipment'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ('location', 'category')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'location'),
                name='unique_name_in_location'
            ),
        )

    def __str__(self):
        return f'{self.name} в {self.location}'

    def save(self, *args, **kwargs):
        cache.delete(f'{self.location_id}{NAME_CACHE_WORKSPACE}')
        cache.delete(f'{self.location_id}{NAME_CACHE_MEETING_ROOM}')
        cache.delete(f'{self.location_id}{NAME_CACHE_LOW_PRICE}')
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete(f'{self.location_id}{NAME_CACHE_WORKSPACE}')
        cache.delete(f'{self.location_id}{NAME_CACHE_MEETING_ROOM}')
        cache.delete(f'{self.location_id}{NAME_CACHE_LOW_PRICE}')
        return super().delete(*args, **kwargs)
