from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
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


@shared_task()
def send_mail_task(user_email, subject, template, add_dict=None):
    """
    Формирует и отправляет эл. письмо.
    """
    data = {'company_name': settings.COMPANY_NAME}
    if add_dict:
        data = {**add_dict, **data}
    html_body = render_to_string(template, data)
    msg = EmailMultiAlternatives(
        subject=subject,
        to=[user_email]
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send()
    return f'{subject} sent'
