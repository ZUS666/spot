from datetime import date

from django.core.exceptions import ValidationError


def validate_birth_day(value):
    if date.today() < value:
        raise ValidationError('Не валидная дата рождения')
