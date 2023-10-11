from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


def validate_birth_day(value):
    if date.today() < value:
        raise ValidationError('Не валидная дата рождения')


@deconstructible
class NamesValidator(RegexValidator):
    regex = r'^[\bА-яа-яёЁA-Za-z][А-яа-яёЁA-Za-z .\'-]*[\bА-яа-яёЁA-Za-z]$'
    message = (
        'Может содержать только буквы, дефисы, точки.'
    )
    flags = 0
