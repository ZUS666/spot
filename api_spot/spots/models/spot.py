from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Spot(models.Model):
    """Класс для cпотов"""
    name = models.TextField(
        "Название коворкинга"
    )
