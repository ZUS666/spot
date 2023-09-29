import datetime

from api_spot.celery import app
from spots.models import Order
from spots.constants import FINISH


@app.task
def repeat_orders_finish():
    """Периодичная заадача, которая завершает заказы который закончились."""
    orders = Order.objects.filter(
        date__lte=datetime.datetime.now().date()
    ).exclude(status=FINISH)
    for order in orders:
        if order.date_finish < datetime.datetime.now():
            order.status = FINISH
            order.save()
    return "Статусы заказов, которые прошли закрились"
