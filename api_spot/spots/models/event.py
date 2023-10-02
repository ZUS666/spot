from django.db import models


class Event(models.Model):
    name = models.CharField('Название Мероприятия', max_length=128)
    image = models.ImageField(
        'Фото',
        upload_to='images/',
    )
    address = models.CharField('Адрес', max_length=255)
    meeting_quantity = models.PositiveSmallIntegerField('Количество мест')
    url = models.URLField('Ссылка')
    date = models.DateField('Дата')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ('date',)

    def __str__(self):
        return self.name
