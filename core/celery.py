import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('book_library')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'change_order_status': {
        'task': 'order.tasks.expired_orders_task',
        'schedule': crontab(minute='00', hour='2')
    },
    'send_mail_expired_order': {
        'task': 'order.tasks.send_mail_expired_orders_task',
        'schedule': crontab(minute='00', hour='10')
    },
}
