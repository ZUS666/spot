from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=128)
    answer = models.TextField()

    class Meta:
        verbose_name = 'Вопрос - ответ'
        verbose_name_plural = 'Выпросы и ответы'

    def __str__(self):
        return self.question[:20]
