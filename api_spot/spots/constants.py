# Review
MIN_EVALUATION = 1
MAX_EVALUATION = 5
# order
MAX_LENGTH_STATUS = 16
MAX_LENGTH_DESC = 100
WAIT_PAY = 'Ожидается оплата'
PAID = 'Оплачено'
ORDER = 'Забранировано'
FINISH = 'Завершен'
NOT_PAID = 'Не оплачено'
ORDER_STATUS_CHOICES = (
    (WAIT_PAY, WAIT_PAY),
    (PAID, PAID),
    (ORDER, ORDER),
    (NOT_PAID, NOT_PAID)
)

# Price
MIN_VALUE = 1
ZERO = 0
MAX_DISCOUNT = 100
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
