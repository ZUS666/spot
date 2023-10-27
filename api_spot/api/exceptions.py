from rest_framework import exceptions


class EmailNotFoundError(exceptions.ValidationError):
    default_code = 'email not found'
    default_detail = {
        'error': 'Этот адрес не зарегистрирован.'
    }


class ConfirmationCodeInvalidError(exceptions.ValidationError):
    default_code = 'confirmation code invalid'
    default_detail = {
        'error': 'Не действительный код подтверждения.'
    }


class UserIsActiveError(exceptions.ValidationError):
    default_code = 'user is active'
    default_detail = {
        'error': 'Адрес уже подтвержден.'
    }


class OrderStatusError(exceptions.ValidationError):
    default_code = 'order not wait_pay'
    default_detail = {
        'error': 'Заказ не ждет оплаты.'
    }


class AddSpotsError(exceptions.ValidationError):
    default_code = 'unique name in location'
    default_detail = {
        'error': 'Название уже есть в локации'
    }


class SubscribedUserError(exceptions.ValidationError):
    default_code = 'subscribe exists'
    default_detail = {
        'error': 'Вы уже подписаны.'
    }


class NotSubscribedUserError(exceptions.ValidationError):
    default_code = 'subscribe does not exists'
    default_detail = {
        'error': 'Вы не подписаны.'
    }
