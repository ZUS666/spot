from rest_framework import exceptions


class EmailNotFoundError(exceptions.ValidationError):
    default_code = 'email not found'
    default_detail = {
        'error': 'Пользователь с таким email не зарегистрирован'
    }


class ConfirmationCodeInvalidError(exceptions.ValidationError):
    default_code = 'confirmation code invalid'
    default_detail = {
        'error': 'Не действительный код подтверждения'
    }


class UserIsActiveError(exceptions.ValidationError):
    default_code = 'user is active'
    default_detail = {
        'error': 'email подтвержден'
    }
