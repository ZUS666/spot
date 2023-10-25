from django.contrib.auth import get_user_model
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from promo.constants import NEWS_EMAIL_TEMPLATE, PROMOCE_EMAIL_TEMPLATE


User = get_user_model()


def get_list_emails():
    """
    Возращает список пользователей подписанных на рассылку.
    """
    return [User.objects.filter(
        is_subscribed=True).values_list('email', flat=True)
    ]


def get_data_news(text):
    """
    Создание контекста для новостного письма.
    """
    context = {
        'text_message': text
    }
    return context


def get_data_promo(promocode):
    """
    Создание контекста для письма с промокодом.
    """
    context = {
        'promocode': promocode.name,
        'percent_discount': promocode.percent_discount,
        'expiry_data': promocode.expiry_date
    }
    return context


def create_task_after_save_promo_email(obj):
    """
    Принимает объект письма
    """
    import json
    from promo.tasks import create_chunk_task_send_mails

    context = get_data_news(obj.text_message)
    template = NEWS_EMAIL_TEMPLATE
    if obj.promo_code:
        context = {**context, **get_data_promo(obj.promocode)}
        template = PROMOCE_EMAIL_TEMPLATE
    time = ClockedSchedule.objects.create(clocked_time=obj.send_datetime)
    task = PeriodicTask.objects.create(
        name=f'отправка письма {obj.subject_message}',
        task='promo.tasks.create_chunk_task_send_mails',
        clocked=time,
        start_time=obj.send_datetime,
        one_off=True,
        enabled=True,
        args=json.dumps([
            obj.subject_message,
            template,
            context,
        ])
    )
    # task.run_tasks()
    # tasks = [(self.celery_app.tasks.get(task.task),
    #               loads(task.args),
    #               loads(task.kwargs),
    #               task.queue,
    #               task.name)
    #              for task in queryset]