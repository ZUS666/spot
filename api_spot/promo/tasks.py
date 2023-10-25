# from celery
# from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from api_spot.celery import app
from promo.services import get_list_emails


@app.task
def send_mail_news(user_email, subject, template, data, *args, **kwargs):
    """
    Формирует и отправляет эл. письмо.
    """
    html_body = render_to_string(template, data)
    msg = EmailMultiAlternatives(
        subject=subject,
        to=[user_email]
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send()
    return f'email {subject} sent to {user_email}'


@app.task
def create_chunk_task_send_mails(*args, **kwargs):
    from information.models import Question
    Question.objects.create(question='asdsad', answer='asdasd')
    # list_emails = get_list_emails()
    # send_mail_news.chunks(
    #     {
    #         'user_email': email,
    #         # ''
    #     } for email in list_emails
    # )
    # print(subject)
    print(*args)
    print(**kwargs)
