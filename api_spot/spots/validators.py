import datetime

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

import spots.constants as constants


def date_gt_two_months(date: datetime.datetime) -> None:
    """Проверка что дата больше чем через MAX_COUNT_DAYS дней."""
    if date > (
        datetime.datetime.now() + datetime.timedelta(
            days=constants.MAX_COUNT_DAYS
        )
    ).date():
        raise ValidationError({
            'date': 'Нельзя забронировать на '
                    f'{constants.MAX_COUNT_DAYS} дней вперед.'
        })


def date_time_lt_now(date_time: datetime.datetime) -> None:
    """Проверка что время меньше текущего."""
    if date_time < datetime.datetime.now():
        raise ValidationError({
            'start_time': 'Нельзя забронировать в прошлом.'
        })


def time_in_location_time(start_time, end_time, location) -> None:
    """Проверка что время в границах открытия локации."""
    if start_time < location.open_time:
        raise ValidationError({
            'start_time': 'Локация еще не будет открыта'
        })
    if end_time > location.close_time:
        raise ValidationError({
            'end_time': 'Локация уже будет закрыта'
        })


def start_lte_end(start_time, end_time) -> None:
    """Проверка что конец брони позже начала."""
    if end_time <= start_time:
        raise ValidationError({
            'end_time': 'Конец брони должен быть позже начала'
        })


def date_in_location_date(date, location) -> None:
    """Проверка что date в границах открытия локации."""
    index = int(location.days_open[0])
    days = constants.DAYS_CHOICES[index][0]
    last_day = days[-2:]
    int_last_day = constants.DAYS_DICT[last_day]
    if date.weekday() > int_last_day:
        raise ValidationError({
            'date': 'В данный день закрыто'
        })


def check_date_time(self) -> None:
    """Проверка дат."""
    date_gt_two_months(self.date)
    date_time = datetime.datetime.strptime(
        f'{self.date} {self.start_time}', '%Y-%m-%d %H:%M:%S'
    )
    date_time_lt_now(date_time)
    date_in_location_date(self.date, self.spot.location)
    time_in_location_time(self.start_time, self.end_time, self.spot.location)
    start_lte_end(self.start_time, self.end_time)


def check_spot_order(self) -> None:
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
