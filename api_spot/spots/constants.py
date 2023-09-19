import datetime

MIN_EVALUATION = 1
MAX_EVALUATION = 5
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
MINUTES = 'minutes'
TIME_CHOICES = tuple([
    (
        datetime.time(x).isoformat(MINUTES),
        f'{datetime.time(x).isoformat(MINUTES)} -'
        f'{datetime.time(x + 1).isoformat(MINUTES)}'
    )
    for x in range(8, 20)
])
