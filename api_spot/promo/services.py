from django.contrib.auth import get_user_model

from promo.models import Promocode


User = get_user_model()


def get_list_emails():
    """
    Возращает список пользователей подписанных на рассылку.
    """
    return list(User.objects.filter(
        is_subscribed=True).values_list('email', flat=True))


def get_data_news(text_message):
    """
    Создание контекста для новостного письма.
    """
    context = {
        'text_message': text_message
    }
    return context


def get_data_promo(promocode_id):
    """
    Создание контекста для письма с промокодом.
    """
    promocode = Promocode.objects.get(id=promocode_id)
    context = {
        'promocode_name': promocode.name,
        'percent_discount': promocode.percent_discount,
        'expiry_date': promocode.expiry_date
    }
    return context
