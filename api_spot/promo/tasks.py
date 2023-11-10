from api.tasks import send_mail_task
from api_spot.celery import app
from promo.models import EmailNews
from promo.services import get_list_emails


@app.task
def create_chunk_task_send_mail(subject_message, template, context):
    """
    Создает chunk для отправки писем.
    """
    emails = get_list_emails()
    chunk = [(email, subject_message, template, context) for email in emails]
    task = send_mail_task.chunks((chunk), 5).apply_async()
    change_email_status.delay(subject_message)
    return task.ready()


@app.task
def change_email_status(subject_message):
    """
    Меняет статус письма.
    """
    EmailNews.objects.filter(
        subject_message=subject_message).update(is_sent=True)
