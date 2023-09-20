MIN_EVALUATION = 1
MAX_EVALUATION = 5
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
