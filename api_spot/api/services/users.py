import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from ..constants import (FINISH_ACTIVATION_TEMAPLATE,
                         FINISH_RESET_PASSWORD_TEMPLATE, REGISTRATION_TEMPLATE,
                         RESET_PASSWORD_TEMPLATE,
                         SUBJECT_EMAIL_FINISH_ACTIVATION,
                         SUBJECT_EMAIL_FINISH_RESET_PASSWORD,
                         SUBJECT_EMAIL_REGISTRATION,
                         SUBJECT_EMAIL_RESET_PASSWORD)
from ..tasks import send_mail_task

User = get_user_model()


def create_confirmation_code():
    """
    Возращает случайное шестизначное число.
    """
    return int(str(uuid.uuid4().int)[:settings.LEN_CONFIRMATION_CODE])


def get_user_with_email_or_bad_request(email):
    user = User.objects.filter(email=email).first()
    if not user:
        return Response(
            {'error': 'Пользователя с таким email не существует'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return user


def send_templated_mail(user_email, subject, template, add_dict=None):
    """
    Формирует и отправляет эл. письмо.
    """
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
    """
    Вызывает отправку эл. письма с кодом подтверждения.
    """
    data = {'confirmation_code': confirmation_code}
    send_mail_task.delay(
        user_email,
        SUBJECT_EMAIL_REGISTRATION,
        REGISTRATION_TEMPLATE,
        data
    )


def finish_activation_email(user_email):
    """
    Вызывает отправку эл. письма о завершении регистрации.
    """
    send_mail_task.delay(
        user_email,
        SUBJECT_EMAIL_FINISH_ACTIVATION,
        FINISH_ACTIVATION_TEMAPLATE,
    )


def reset_password_email(confirmation_code, user_email):
    data = {'confirmation_code': confirmation_code}
    send_mail_task.delay(
        user_email,
        SUBJECT_EMAIL_RESET_PASSWORD,
        RESET_PASSWORD_TEMPLATE,
        data
    )


def finish_reset_password_email(user_email):
    """
    Вызывает отправку эл. письма о завершении сброса пароля.
    """
    send_mail_task.delay(
        user_email,
        SUBJECT_EMAIL_FINISH_RESET_PASSWORD,
        FINISH_RESET_PASSWORD_TEMPLATE,
    )


def cache_and_send_confirmation_code(user, email_func):
    """
    Кеширует и вызывает функцию отправки письма c кодом подтверждения.
    """
    confirmation_code = create_confirmation_code()
    cache.set(user.id, confirmation_code, settings.TIMEOUT_CACHED_CODE)
    email_func(confirmation_code, user.email)
