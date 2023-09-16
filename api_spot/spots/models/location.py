from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Location(models.Model):
    """Класс для cпотов"""
    street = models.CharField(
        "Название улицы",
        max_length=20,
    )
