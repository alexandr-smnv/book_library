import datetime

from celery import shared_task

from order.models import EXPIRED, Order
from order.utils import send_email_about_cancel_order, send_expired_email


@shared_task()
def expired_orders_task():
    """
    Контроль количества просроченных заказов за прошедшие сутки
    """
    count = 0
    new = 0
    for order in Order.objects.expired_orders():
        count += 1
        if order.status != EXPIRED:
            new += 1
            order.order_expired()
    return f'По состоянию на {datetime.date.today()} всего просроченных заказов - {count} шт.' \
           f'За последние сутки просрочено заказов - {new} шт.'


@shared_task()
def cancel_orders_task():
    """Контроль количества отмененных заказов за прошедшие сутки"""
    count = 0
    for order in Order.objects.cancel_waiting():
        order.order_cancel()
        count += 1
    return f'За последние сутки истек срок ожидания заказов - {count} шт.'


@shared_task()
def send_mail_expired_orders_task():
    """
    Отправка сообщений пользователям, имеющим просроченные заказы
    """
    # Все просроченные заказы
    expired_orders = Order.objects.filter(status=4)
    # Множество с пользователями, имеющими просроченные заказы (пользователи не повторяются)
    users = {order.user for order in expired_orders}
    for user in users:
        # Все просроченные заказы у пользователя
        # Для того, чтобы в одно сообщение занести данные о всех просроченных заказах пользователя
        ex_ord_user = expired_orders.filter(user=user)
        send_expired_email(user, ex_ord_user)


@shared_task()
def send_mail_cancel_order_task():
    """
    Отправка сообщения об отмене заказа по причине превышения времени ожидания
    """
    # Все заказы с истекшим сроком ожидания
    waiting_orders = Order.objects.cancel_waiting()
    # Пользователи имеющие такие заказы
    users = {order.user for order in waiting_orders}
    for user in users:
        # Истекшие заказы у каждого пользователя
        orders = waiting_orders.filter(user=user)
        send_email_about_cancel_order(user, orders)
