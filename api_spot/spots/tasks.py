import datetime

from api_spot.celery import app
from spots.constants import FINISH, PAID
from spots.models import Order


@app.task
def repeat_orders_finish() -> str:
    """Периодичная задача, которая завершает заказы, которые закончились."""
    hour = int(datetime.datetime.now().time().isoformat('hours'))
    Order.objects.filter(
        date__lte=datetime.datetime.now().date(),
        end_time=datetime.time(hour),
        status=PAID
    ).update(status=FINISH)
    return "Статусы заказов, которые закончились изменены"
