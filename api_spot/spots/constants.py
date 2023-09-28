import datetime

# Review
MIN_EVALUATION = 1
MAX_EVALUATION = 5
# order
SECONDS_IN_HOUR = 60 * 60
MAX_LENGTH_STATUS = 16
MAX_LENGTH_DESC = 100
WAIT_PAY = 'Ожидается оплата'
PAID = 'Оплачено'
FINISH = 'Завершен'
CANCEL = 'Отменен'
NOT_PAID = 'Не оплачено'
ORDER_STATUS_CHOICES = (
    (WAIT_PAY, WAIT_PAY),
    (NOT_PAID, NOT_PAID),
    (PAID, PAID),
    (FINISH, FINISH),
    (CANCEL, CANCEL)
)
MINUTES = 'minutes'
START_CHOICES = tuple([
    (
        datetime.time(x),
        datetime.time(x).isoformat(MINUTES)
    )
    for x in range(0, 23)
])
END_CHOICES = tuple([
    (
        datetime.time(x),
        datetime.time(x - 1, 55).isoformat(MINUTES)
    )
    for x in range(1, 24)
])
MAX_COUNT_DAYS = 60
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

# Spot
WORK_SPACE = 'Рабочее место'
MEETING_ROOM = 'Переговорная'
CATEGORY_CHOICES = (
    (WORK_SPACE, WORK_SPACE),
    (MEETING_ROOM, MEETING_ROOM),
)
