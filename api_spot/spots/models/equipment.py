from django.db import models


class Equipment(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название оборудования'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудования'

    def __str__(self):
        return self.name
