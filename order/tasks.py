from celery import shared_task

from order.models import Order
from order.utils import send_expired_email


@shared_task()
def expired_orders_task():
    count = 0
    for order in Order.object.expired_orders():
        order.order_expired()
        count += 1
    return f'У {count} заказов был изменен статус!'


@shared_task()
def send_mail_expired_orders_task():
    expired_orders = Order.object.filter(status=4)
    users = {order.user for order in expired_orders}
    for user in users:
        ex_ord_user = expired_orders.filter(user=user)
        send_expired_email(user, ex_ord_user)
