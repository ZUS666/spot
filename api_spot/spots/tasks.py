import datetime

from celery import shared_task
from django.shortcuts import get_object_or_404

from api.services.orders import order_finished_email
from api_spot.celery import app
from spots.constants import FINISH, NOT_PAID, PAID, WAIT_PAY

from .models.order import Order


@shared_task
def change_status_task(order_id: int) -> str:
    """Таска изменения статуса после n секнуд."""
    order = get_object_or_404(Order, pk=order_id)
    if order.status != PAID and order.status == WAIT_PAY:
        order.status = NOT_PAID
        order.save()
        return f'Cтатус у {order_id} изменен'
    return f'Cтатус у {order_id} не изменен'


@app.task
def repeat_orders_finish() -> str:
    """Периодичная задача, которая завершает заказы, которые закончились."""
    hour = int(datetime.datetime.now().time().isoformat('hours'))
    orders = Order.objects.filter(
        date__lte=datetime.datetime.now().date(),
        end_time=datetime.time(hour),
        status=PAID
    )
    for order in orders:
        order.status = FINISH
        order.save()
        order_finished_email(order)
    return "Статусы заказов, которые закончились изменены"
