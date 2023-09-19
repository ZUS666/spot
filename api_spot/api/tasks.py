from django.shortcuts import get_object_or_404

from time import sleep
from celery import shared_task

from spots.models.order import Order
from spots.constants import NOT_PAID, PAID
from django.conf import settings


@shared_task()
def change_status_task(order_id):
    """Таска изменения статуса после n секнуд."""
    sleep(settings.TIME_CHANGE_STATUS)
    order = get_object_or_404(Order, pk=order_id)
    if order.status != PAID:
        order.status = NOT_PAID
        order.save()
        print("Status changed")
