import uuid

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ..constants import (REGISTRATION_TEMPLATE, SUBJECT_EMAIL_REGISTRATION,
                         SUBJECT_EMAIL_FINISH_ACTIOVATION,
                         FINISH_ACTIOVATION_EMAIL)


def create_confirmation_code():
    """
    Возращает случайное шестизначное число.
    """
    return str(uuid.uuid4().int)[:settings.LEN_CONFIRMATION_CODE]


def send_templated_mail(user_email, subject, template, add_dict=None):
    data = {'company_name': settings.COMPANY_NAME}
    if add_dict:
        data = {**add_dict, **data}
    html_body = render_to_string(template, data)
    msg = EmailMultiAlternatives(
        subject=subject,
        to=[user_email]
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send()


def registration_email(confirmation_code, user_email):
    data = {'confirmation_code': confirmation_code}
    send_templated_mail(
        user_email,
        SUBJECT_EMAIL_REGISTRATION,
        REGISTRATION_TEMPLATE,
        data
    )


def cache_and_send_confirmation_code(user):
    """
    Кеширует и вызывает функцию отправки письма.
    """
    confirmation_code = create_confirmation_code()
    cache.set(user.id, confirmation_code, settings.TIMEOUT_CACHED_CODE)
    registration_email(confirmation_code, user.email)


def finish_activation_email(user_email):
    send_templated_mail(
        user_email,
        SUBJECT_EMAIL_FINISH_ACTIOVATION,
        FINISH_ACTIOVATION_EMAIL,
    )
