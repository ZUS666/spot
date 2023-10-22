import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.authtoken.models import Token

from api.constants import (
    FINISH_ACTIVATION_TEMAPLATE, FINISH_RESET_PASSWORD_TEMPLATE,
    REGISTRATION_TEMPLATE, RESET_PASSWORD_TEMPLATE,
    SUBJECT_EMAIL_FINISH_ACTIVATION, SUBJECT_EMAIL_FINISH_RESET_PASSWORD,
    SUBJECT_EMAIL_REGISTRATION, SUBJECT_EMAIL_RESET_PASSWORD,
)
from api.exceptions import (
    ConfirmationCodeInvalidError, EmailNotFoundError, UserIsActiveError,
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
    """
    Получение информации о пользователе для отправки письма.
    """
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return data


def activation_user_service(validated_data):
    """
    Логика активации пользователя.
    """
    email = validated_data.get('email')
    confirmation_code = validated_data.get('confirmation_code')
    user = User.objects.filter(email=email).first()
    if not user:
        raise EmailNotFoundError
    if confirmation_code != cache.get(user.id):
        raise ConfirmationCodeInvalidError
    user.is_active = True
    user.save()
    finish_activation_email(user)
    cache.delete(user.id)


def change_password_service(validated_data):
    """
    Логика изменения пароля пользователя.
    """
    password = validated_data.get('password')
    user = validated_data.get('user')
    user.set_password(password)
    user.save(update_fields=['password'])


def reset_password_service(validated_data):
    """
    Логика сброса пароля через код подтверждения.
    """
    email = validated_data.get('email')
    confirmation_code = validated_data.get('confirmation_code')
    password = validated_data.get('password')
    user = User.objects.filter(email=email).first()
    if not user:
        raise EmailNotFoundError
    if confirmation_code != cache.get(user.id):
        raise ConfirmationCodeInvalidError
    user.set_password(password)
    user.save(update_fields=['password'])
    token = Token.objects.filter(user=user).exists()
    if token:
        token.delete()
    cache.delete(user.id)
    finish_reset_password_email(user)


def reset_password_confirmation_code_service(validated_data):
    """
    Логика запроса на сброс пароля пользователя.
    """
    email = validated_data.get('email')
    user = User.objects.filter(email=email).first()
    if not user:
        raise EmailNotFoundError
    cache_and_send_confirmation_code(user, reset_password_email)


def resend_confirmation_code_service(validated_data):
    """
    Логика повторной отправки кода подтверждения.
    """
    email = validated_data.get('email')
    user = User.objects.filter(email=email).first()
    if not user:
        raise EmailNotFoundError
    if user.is_active:
        raise UserIsActiveError
    cache_and_send_confirmation_code(user, registration_email)
