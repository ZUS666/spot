from django.db import models

from .price import Price
from .location import Location
from .category import Category
from .equipment import Equipment


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
    main_photo = models.ImageField(
        upload_to='images/',
        verbose_name='Фото рабочего места',
        help_text='Основное фото рабочего места'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='spots',
        verbose_name='Локация',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='spots',
        verbose_name='Категория',
    )
    equipment = models.ManyToManyField(
        Equipment,
        related_name='spots',
        verbose_name='Оборудование'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание'
    )
    number = models.IntegerField(
        'Номер комнаты'
    )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        constraints = (
            models.UniqueConstraint(
                fields=('category', 'number'),
                name='unique_category_number_spot'
            ),
        )

    def __str__(self):
        return self.name
