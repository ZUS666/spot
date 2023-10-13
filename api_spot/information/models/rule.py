from django.db import models


class Rule(models.Model):
    """
    Модель для Правила использования сервиса.
    """
    title = models.CharField('Правило', max_length=255)
    text = models.TextField('Текст правила',)

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'

    def __str__(self):
        return self.title[:20]
