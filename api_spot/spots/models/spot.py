from django.db import models

from spots.constants import CATEGORY_CHOICES
from spots.models import Equipment
from spots.models.location import Location
from spots.models.price import Price
from spots.services import delete_location_cache_in_spot


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
        verbose_name='Описание',
        blank=True,
        null=True
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
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        delete_location_cache_in_spot(self.location_id)
        return super().save(*args, **kwargs)
