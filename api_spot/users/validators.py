from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class TelegramUsernameValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z][\w]{4,31}$',
    message = (
        'Имя пользователя в Telegram должно содержать'
        'только буквы, цифры и символ подчеркивания,'
        'начинаться с буквы и быть длиной от 5 до 32 символов.',
    )
    flags = 0
