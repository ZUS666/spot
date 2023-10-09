from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


def validate_birth_day(value):
    if date.today() < value:
        raise ValidationError('Не валидная дата рождения')


@deconstructible
class NamesValidator(RegexValidator):
    regex = r"^[^0-9_!¡?÷?¿/+=@#$%^&*(){}|~<>,;:[\]]+$"
    message = (
        "Не может содержать цифры и знаки кроме: .'-"
    )
    flags = 0
