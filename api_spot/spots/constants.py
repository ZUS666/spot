import datetime

# Review
MIN_EVALUATION: int = 1
MAX_EVALUATION: int = 5
# order
SECONDS_IN_HOUR: int = 60 * 60
MAX_LENGTH_STATUS: int = 16
MAX_LENGTH_DESC: int = 100
WAIT_PAY: str = 'Ожидается оплата'
PAID: str = 'Оплачено'
FINISH: str = 'Завершен'
CANCEL: str = 'Отменен'
NOT_PAID: str = 'Не оплачено'
ORDER_STATUS_CHOICES: tuple[str, str] = (
    (WAIT_PAY, WAIT_PAY),
    (NOT_PAID, NOT_PAID),
    (PAID, PAID),
    (FINISH, FINISH),
    (CANCEL, CANCEL)
)
MINUTES: str = 'minutes'
START_CHOICES: tuple[datetime.time, datetime.time] = tuple([
    (
        datetime.time(x),
        datetime.time(x).isoformat(MINUTES)
    )
    for x in range(0, 24)
])
END_CHOICES: tuple[datetime.time, datetime.time] = tuple([
    (
        datetime.time(x),
        datetime.time(x - 1, 55).isoformat(MINUTES)
    )
    if x != 24 else (
        datetime.time(0),
        datetime.time(23, 55).isoformat(MINUTES)
    )
    for x in range(1, 25)
])
MAX_COUNT_DAYS: int = 60
# Price
MIN_VALUE = 1
ZERO = 0
MAX_DISCOUNT = 70
MAX_DISCOUNT_MESSAGE = f'Скидка не может превышать {MAX_DISCOUNT}%'
DISCOUNT_NEGATIVE_MESSAGE = 'Скидка не может быть меньше нуля.'
PRICE_NEGATIVE_OR_ZERO_MESSAGE = 'Цена не может быть меньше или равна нулю.'

# Location
LAT_MAX = 90
LAT_MIN = -90
LAT_MSG_ERROR = 'Широта должна быть в диапазоне от -90 до 90'
LONG_MAX = 180
LONG_MIN = -180
LONG_MSG_ERROR = 'Долгота должна быть в диапазоне от -180 до 180'
NAME_CACHE_WORKSPACE = 'workspace'
NAME_CACHE_MEETING_ROOM = 'meeting_room'
NAME_CACHE_RATING = 'rating'
NAME_CACHE_LOW_PRICE = 'low_price'
DAYS_CHOICES: tuple[str, str] = (
    ('пн-вс', 'пн-вс'),
    ('пн-сб', 'пн-сб'),
    ('пн-пт', 'пн-пт'),
)
DAYS_DICT = {
    'вс': 6,
    'сб': 5,
    'пт': 4,
}

# Spot
WORK_SPACE = 'Рабочее место'
MEETING_ROOM = 'Переговорная'
CATEGORY_CHOICES = (
    (WORK_SPACE, WORK_SPACE),
    (MEETING_ROOM, MEETING_ROOM),
)
