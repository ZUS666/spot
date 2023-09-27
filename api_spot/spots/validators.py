import datetime

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

import spots.constants as constants


def check_date_time(self):
    """Проверка дат."""
    if self.date > (
        datetime.datetime.now() + datetime.timedelta(
            days=constants.MAX_COUNT_DAYS
        )
    ).date():
        raise ValidationError({
            'date': 'Нельзя забронировать на 60 дней вперед.'
        })
    date_time_now = datetime.datetime.strptime(
        f'{self.date} {self.start_time}', '%Y-%m-%d %H:%M:%S'
    )
    if date_time_now < datetime.datetime.now():
        raise ValidationError({
            'start_time': 'Нельзя забронировать в прошлом.'
        })
    if date_time_now < datetime.datetime.now():
        raise ValidationError({
            'start_time': 'Нельзя забронировать в прошлом.'
        })

    if self.start_time < self.spot.location.open_time:
        raise ValidationError({
            'start_time': 'Локация еще не будет открыта'
        })
    if self.end_time > self.spot.location.close_time:
        raise ValidationError({
            'end_time': 'Локация уже будет закрыта'
        })

    if self.end_time == self.start_time:
        raise ValidationError({
            'end_time': 'Конец брони не может совпадать с началом'
        })
    if self.end_time < self.start_time:
        raise ValidationError({
            'end_time': 'Конец брони должен быть позже начала'
        })


def check_spot_order(self):
    """Проверка на то, что данный спот свободен в данное время."""
    qs = self.__class__._default_manager.exclude(
        status__in=[constants.CANCEL, constants.FINISH]
    ).filter(
        spot=self.spot,
        date=self.date,
        start_time__lt=self.end_time,
        end_time__gt=self.start_time
    ).exclude(pk=self.pk)
    if qs.exists():
        raise ValidationError({
            NON_FIELD_ERRORS: 'Данный коворкинг уже забронирован',
        })
