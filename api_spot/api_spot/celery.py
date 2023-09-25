import os

from celery import Celery

app_name = "api_spot"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{app_name}.settings")
app = Celery(app_name, broker='redis://redis:6379/0')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
