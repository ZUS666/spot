from django.utils import timezone
from rest_framework.exceptions import ValidationError

from promo.models import Promocode


def promocode_available_check(value):
    promocode = Promocode.objects.filter(name=value).first()
    if promocode:
        if promocode.balance < 1:
            raise ValidationError('Количество использований исчерпано.')
        if promocode.expiry_date < timezone.now().date():
            raise ValidationError('Срок годности промокода истек.')
