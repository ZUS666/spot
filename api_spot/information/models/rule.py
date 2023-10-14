from django.core.validators import FileExtensionValidator
from django.db import models
from ckeditor.fields import RichTextField


class Rule(models.Model):
    """
    Модель для Правила использования сервиса.
    """
    title = models.CharField('Правило', max_length=255)
    text = RichTextField('Текст правила',)
    icon = models.FileField(
        upload_to='icons/rules/',
        validators=(FileExtensionValidator(('svg',)),)
    )

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'

    def __str__(self):
        return self.title[:20]
