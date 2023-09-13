import random

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ..constants import (REGISTRATION_TEMPLATE, SUBJECT_EMAIL_REGISTRATION,
                         TIMEOUT_CACHED_CODE)


def create_confirmation_code():
    """
    Возращает случайное шестизначное число.
    """
    return str(random.randint(100000, 999999))


def registration_email(confirmation_code, user_email):
    """
    Формирует и отправляет письмо с кодом подтверждения.
    """
    data = {'confirmation_code': confirmation_code}
    html_body = render_to_string(REGISTRATION_TEMPLATE, data)
    msg = EmailMultiAlternatives(
        subject=SUBJECT_EMAIL_REGISTRATION,
        to=[user_email]
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send()


def cache_and_send_confirmation_code(user):
    """
    Кеширует и вызывает функцию отправки письма.
    """
    confirmation_code = create_confirmation_code()
    cache.set(user.id, confirmation_code, TIMEOUT_CACHED_CODE)
    registration_email(confirmation_code, user.email)
