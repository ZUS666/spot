from django.shortcuts import get_object_or_404

from time import sleep
from celery import shared_task

from spots.models.order import Order, LOCK, PAID


@shared_task()
def change_status_task(order_id):
    """Таска изменения статуса после 60*1 секнуд."""
    sleep(60 * 1)  # Simulate expensive operation(s) that freeze Django
    order = get_object_or_404(Order, pk=order_id)
    if order.status != PAID:
        order.status = LOCK
        order.save()
        print("Status changed")
    print("KEKwait")
