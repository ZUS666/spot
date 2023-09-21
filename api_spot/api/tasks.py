from celery import shared_task
from django.shortcuts import get_object_or_404

from spots.constants import NOT_PAID, PAID
from spots.models.order import Order


@shared_task()
def change_status_task(order_id):
    """Таска изменения статуса после n секнуд."""
    order = get_object_or_404(Order, pk=order_id)
    if order.status != PAID:
        order.status = NOT_PAID
        order.save()
        print("Status changed")
