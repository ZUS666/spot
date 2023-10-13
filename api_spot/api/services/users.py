import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

from api.constants import (
    FINISH_ACTIVATION_TEMAPLATE, FINISH_RESET_PASSWORD_TEMPLATE,
    REGISTRATION_TEMPLATE, RESET_PASSWORD_TEMPLATE,
    SUBJECT_EMAIL_FINISH_ACTIVATION, SUBJECT_EMAIL_FINISH_RESET_PASSWORD,
    SUBJECT_EMAIL_REGISTRATION, SUBJECT_EMAIL_RESET_PASSWORD,
)
from api.tasks import send_mail_task


User = get_user_model()


def create_confirmation_code():
    """
    Возращает случайное шестизначное число.
    """
    return int(str(uuid.uuid4().int)[:settings.LEN_CONFIRMATION_CODE])


def registration_email(context, user):
    """
    Вызывает отправку эл. письма с кодом подтверждения.
    """
    context = {**context, **get_user_email_context(user)}
    send_mail_task.delay(
        user.email,
        SUBJECT_EMAIL_REGISTRATION,
        REGISTRATION_TEMPLATE,
        context
    )


def finish_activation_email(user):
    """
    Вызывает отправку эл. письма о завершении регистрации.
    """
    context = get_user_email_context(user)
    send_mail_task.delay(
        user.email,
        SUBJECT_EMAIL_FINISH_ACTIVATION,
        FINISH_ACTIVATION_TEMAPLATE,
        context
    )


def reset_password_email(context, user):
    context = {**context, **get_user_email_context(user)}
    send_mail_task.delay(
        user.email,
        SUBJECT_EMAIL_RESET_PASSWORD,
        RESET_PASSWORD_TEMPLATE,
        context
    )


def finish_reset_password_email(user):
    """
    Вызывает отправку эл. письма о завершении сброса пароля.
    """
    context = get_user_email_context(user)
    send_mail_task.delay(
        user.email,
        SUBJECT_EMAIL_FINISH_RESET_PASSWORD,
        FINISH_RESET_PASSWORD_TEMPLATE,
        context
    )


def cache_and_send_confirmation_code(user, email_func):
    """
    Кеширует и вызывает функцию отправки письма c кодом подтверждения.
    """
    confirmation_code = create_confirmation_code()
    cache.set(user.id, confirmation_code, settings.TIMEOUT_CACHED_CODE)
    context = {'confirmation_code': confirmation_code}
    email_func(context, user)


def get_user_email_context(user):
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return data
