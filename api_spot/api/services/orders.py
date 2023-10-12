from api.constants import (
    ORDER_CANCEL_TEMPLATE, ORDER_CONFIRMATION_TEMPLATE, ORDER_FINISH_TEMPLATE,
    SUBJECT_EMAIL_ORDER_CANCEL, SUBJECT_EMAIL_ORDER_CONFRIMATION,
    SUBJECT_EMAIL_ORDER_FINISH,
)
from api.services.users import get_user_email_context
from api.tasks import send_mail_task
from spots.constants import CANCEL, NOT_PAID


def is_ordered_spot(instance, date, start_time, end_time):
    """
    Получение информации о наличии бронирований в заданный
    промежуток даты и времени.
    """
    return instance.orders.exclude(status__in=[CANCEL, NOT_PAID]).filter(
        date=date,
        start_time__lt=end_time,
        end_time__gt=start_time,
    ).exists()


def get_order_context(order):
    """
    Получение контекста для писем с информацией о бронировании.
    """
    spot = order.spot
    location = spot.location
    full_address = location.get_full_address_str()
    data = {
        'location_name': location.name,
        'full_address': full_address,
        'spot_name': spot.name,
        'date': order.date,
        'start_time': order.start_time,
        'end_time': order.end_time,
    }
    return data


def order_confirmation_email(order):
    """
    Вызывает функцию отправки письма о подтверждении бронировани
    с добавленим контекста.
    """
    user = order.user
    context = {
        **get_user_email_context(user),
        **get_order_context(order),
    }
    send_mail_task.delay(
        user.email,
        SUBJECT_EMAIL_ORDER_CONFRIMATION,
        ORDER_CONFIRMATION_TEMPLATE,
        context
    )


def order_cancel_email(order):
    """
    Вызывает функцию отправки письма об отмене бронирования
    с добавленим контекста.
    """
    user = order.user
    context = {
        **get_user_email_context(user),
        **get_order_context(order),
    }
    send_mail_task.delay(
        user.email,
        SUBJECT_EMAIL_ORDER_CANCEL,
        ORDER_CANCEL_TEMPLATE,
        context
    )


def order_finished_email(order):
    """
    Вызывает функцию отправки письма после бронирования
    с добавленим контекста.
    """
    user = order.user
    context = {
        **get_user_email_context(user),
        **get_order_context(order),
    }
    send_mail_task.delay(
        user.email,
        SUBJECT_EMAIL_ORDER_FINISH,
        ORDER_FINISH_TEMPLATE,
        context
    )
