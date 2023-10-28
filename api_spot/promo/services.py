import json

from django.contrib.auth import get_user_model
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from promo.constants import NEWS_EMAIL_TEMPLATE, PROMOCE_EMAIL_TEMPLATE


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


def get_data_promo(promocode):
    """
    Создание контекста для письма с промокодом.
    """
    context = {
        'promocode_name': promocode.name,
        'percent_discount': promocode.percent_discount,
        'expiry_date': promocode.expiry_date.isoformat(),
    }
    return context


def create_task_after_save_promo_email(obj):
    """
    Принимает объект письма
    """
    context = get_data_news(obj.text_message)
    template = NEWS_EMAIL_TEMPLATE
    if obj.promocode:
        context = {**context, **get_data_promo(obj.promocode)}
        template = PROMOCE_EMAIL_TEMPLATE
    time = ClockedSchedule.objects.create(clocked_time=obj.send_datetime)
    task = PeriodicTask.objects.create(
        name=f'Email subject:{obj.subject_message} '
             f'date:{obj.send_datetime.date().isoformat()}',
        task='promo.tasks.create_chunk_task_send_mail',
        clocked=time,
        one_off=True,
        args=json.dumps([
            obj.subject_message,
            template,
            context,
        ])
    )
    return task
