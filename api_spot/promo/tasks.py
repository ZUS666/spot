from django.core.mail import EmailMultiAlternatives
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.utils import timezone

from api_spot.celery import app
from promo.constants import NEWS_EMAIL_TEMPLATE, PROMOCE_EMAIL_TEMPLATE
from promo.models import EmailNews
from promo.services import get_data_news, get_data_promo, get_list_emails


@app.task
def send_mail_news(user_email, subject, template, context):
    """
    Формирует и отправляет эл. письмо.
    """
    html_body = render_to_string(template, context)
    msg = EmailMultiAlternatives(
        subject=subject,
        to=[user_email]
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send()
    return f'email {subject} sent to {user_email}'


@app.task
def create_chunk_task_send_mail(email):
    subject_message = email.get('subject_message')
    text_message = email.get('text_message')
    promocode_id = email.get('promocode')
    context = get_data_news(text_message)
    template = NEWS_EMAIL_TEMPLATE
    if promocode_id:
        context = {**context, **get_data_promo(promocode_id)}
        template = PROMOCE_EMAIL_TEMPLATE
    emails = get_list_emails()
    chunk = [(email, subject_message, template, context) for email in emails]
    send_mail_news.chunks((chunk), 5).apply_async()


@app.task
def every_day_check_today_email_task():
    email = EmailNews.objects.filter(
        send_date=timezone.now()
    ).first()
    dict_email = model_to_dict(email)
    if email:
        create_chunk_task_send_mail(dict_email)
        email.is_sent = True
        email.save()
        return f'{email.subject_message} sent'
    return 'There are no emails to send today'
