from django.shortcuts import get_object_or_404

from time import sleep
from celery import shared_task

from spots.models.order import Order, LOCK, PAID
from api.constants import TIME_CHANGE_STATUS


@shared_task()
def change_status_task(order_id):
    """Таска изменения статуса после n секнуд."""
    sleep(TIME_CHANGE_STATUS)
    order = get_object_or_404(Order, pk=order_id)
    if order.status != PAID:
        order.status = LOCK
        order.save()
        print("Status changed")
    print("KEKwait")
