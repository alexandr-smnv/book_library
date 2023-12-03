from celery import shared_task

from order.models import Order


@shared_task()
def expired_orders_task():
    count = 0
    for order in Order.object.expired_orders():
        order.order_expired()
        count += 1
    return f'У {count} заказов был изменен статус!'
