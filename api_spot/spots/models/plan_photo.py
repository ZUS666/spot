from django.db import models

from spots.models.location import Location


class PlanPhoto(models.Model):
    location = models.OneToOneField(
        Location,
        related_name='plan_photo',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Фото-план',
        blank=False,
        upload_to='images/plans/',
    )

    class Meta:
        verbose_name = 'Фото-план'
        verbose_name_plural = 'Фото-планы'
        ordering = ('location',)

    def __str__(self) -> str:
        return self.location.name
