import os

from celery import Celery
from celery.schedules import crontab


app_name = 'api_spot'
app = Celery(app_name, broker=os.getenv('CELERY_BROKER'))
if os.getenv('DEBUG'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{app_name}.locconf')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{app_name}.settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'every': {
        'task': 'spots.tasks.repeat_orders_finish',
        'schedule': crontab(hour='*/1', minute=1),
    },
}
