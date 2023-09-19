from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Spot(models.Model):
    """Класс для cпотов"""
    name = models.CharField(
        "Название коворкинга",
        max_length=20
    )
