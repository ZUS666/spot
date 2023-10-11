from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class ListNamesValidator(RegexValidator):
    regex = r'^(?:\w+,\s)+[\b\w]+$'
    message = (
        'Названия через запятую c пробелом'
    )
    flags = 0
