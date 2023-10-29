from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils import timezone

from promo.constants import MAX_PROMO_DISCOUNT_MESSAGE


def validate_datetime_less_present(value):
    if value < timezone.now():
        raise ValidationError('Значение должно быть в будущем')


class MaxDiscountValidator(MaxValueValidator):
    message = MAX_PROMO_DISCOUNT_MESSAGE
