import datetime

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

import spots.constants as constants


def date_gt_two_months(date: datetime.datetime, error) -> None:
    """Проверка что дата больше чем через MAX_COUNT_DAYS дней."""
    if date > (
        datetime.datetime.now() + datetime.timedelta(
            days=constants.MAX_COUNT_DAYS
        )
    ).date():
        raise error({
            'date': 'Нельзя забронировать на '
                    f'{constants.MAX_COUNT_DAYS} дней вперед.'
        })


def date_time_lt_now(date_time: datetime.datetime, error) -> None:
    """Проверка что время меньше текущего."""
    if date_time < datetime.datetime.now():
        raise error({
            'start_time': 'Нельзя забронировать в прошлом.'
        })


def time_in_location_time(start_time, end_time, location, error) -> None:
    """Проверка что время в границах открытия локации."""
    if start_time < location.open_time:
        raise error({
            'start_time': 'Локация еще не будет открыта'
        })
    if end_time > location.close_time:
        raise error({
            'end_time': 'Локация уже будет закрыта'
        })


def start_lte_end(start_time, end_time, error) -> None:
    """Проверка что конец брони позже начала."""
    if end_time <= start_time:
        raise error({
            'end_time': 'Конец брони должен быть позже начала'
        })


def date_in_location_date(date, location, error) -> None:
    """Проверка что date в границах открытия локации."""
    index = int(location.days_open[0])
    days = constants.DAYS_CHOICES[index][0]
    last_day = days[-2:]
    int_last_day = constants.DAYS_DICT[last_day]
    if date.weekday() > int_last_day:
        raise error({
            'date': 'В данный день закрыто'
        })


def check_date_time(date, start_time, end_time,
                    location, error=ValidationError) -> None:
    """Проверка дат."""
    date_gt_two_months(date, error)
    date_time = datetime.datetime.strptime(
        f'{date} {start_time}', '%Y-%m-%d %H:%M:%S'
    )
    date_time_lt_now(date_time, error)
    # date_in_location_date(date, location, error)
    time_in_location_time(start_time, end_time, location, error)
    start_lte_end(start_time, end_time, error)


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
