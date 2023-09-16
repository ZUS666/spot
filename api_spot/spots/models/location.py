from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Location(models.Model):
    """Класс для cпотов"""
    street = models.TextField(
        "Название улицы",
    )
