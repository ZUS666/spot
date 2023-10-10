from django.db import models
from django.core.validators import FileExtensionValidator


class Equipment(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название оборудования'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание'
    )
    icon = models.FileField(
        upload_to='icons/equipment/',
        validators=(FileExtensionValidator(('svg',)),)
    )

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудования'

    def __str__(self):
        return self.name


class SpotEquipment(models.Model):
    spot = models.ForeignKey(
        'Spot',
        related_name='spot_equipment',
        on_delete=models.CASCADE
    )
    equipment = models.ForeignKey(
        'Equipment',
        related_name='spot_equipment',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Место и оборудование'
        verbose_name_plural = 'Места и оборудования'
        constraints = (
            models.UniqueConstraint(
                fields=('spot', 'equipment'),
                name='unique_equipment'
            ),
        )

    def __str__(self):
        return f'{self.equipment} к {self.spot}'
