from django.db import models
from django.core.validators import FileExtensionValidator


class Question(models.Model):
    """
    Модель для часто задаваемых вопросов.
    """
    question = models.CharField('Вопрос', max_length=128)
    answer = models.TextField('Ответ',)
    icon = models.FileField(
        upload_to='icons/question/',
        validators=(FileExtensionValidator(('svg',)),)
    )

    class Meta:
        verbose_name = 'Вопрос - ответ'
        verbose_name_plural = 'Выпросы и ответы'

    def __str__(self):
        return self.question[:20]
