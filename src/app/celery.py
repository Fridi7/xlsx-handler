import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xlsx_handler.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
