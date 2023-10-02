from django.db import models


class Rule(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'

    def __str__(self):
        return self.title[:20]
