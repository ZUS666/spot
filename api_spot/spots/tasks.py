import datetime

from api_spot.celery import app
from spots.models import Order
from spots.constants import FINISH, CANCEL


@app.task
def repeat_orders_finish():
    """Периодичная задача, которая завершает заказы, которые закончились."""
    hour = int(datetime.datetime.now().time().isoformat('hours'))
    orders = Order.objects.filter(
        date__lte=datetime.datetime.now().date(),
        end_time=datetime.time(hour)
    ).exclude(status__in=[FINISH, CANCEL])
    for order in orders:
        order.status = FINISH
        order.save()
    return "Статусы заказов, которые закончились изменены"
