import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('book_library')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every-day-in-23-00': {
        'task': 'order.tasks.expired_orders_task',
        'schedule': crontab(minute='16', hour='14')
    },
}
