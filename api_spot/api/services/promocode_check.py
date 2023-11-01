from django.utils import timezone
from rest_framework.exceptions import ValidationError

from promo.models import Promocode


def promocode_available_check(promocode_name, spot, user):
    """
    Проверка доступности использования промокода.
    """
    promocode = Promocode.objects.filter(name=promocode_name).first()
    if promocode:
        if promocode.balance < 1:
            raise ValidationError('Количество использований исчерпано.')
        if promocode.expiry_date < timezone.now().date():
            raise ValidationError('Срок годности промокода истек.')
        if (promocode.only_category
                and promocode.only_category != spot.category):
            raise ValidationError('Промокод не применяется для этой категории')
        used_by_user = promocode.promocode_user.filter(user=user).exists()
        if promocode.one_off and used_by_user:
            raise ValidationError('Вы уже использовали данный промокод')
        return promocode
    else:
        raise ValidationError('Промокода не существует')
