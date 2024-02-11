import datetime

from django.db import models
from django.db.models import Q
from django.utils import timezone

from users.models import User

REVIEW = 0
READY = 1
RENTED = 2
RETURNED = 3
EXPIRED = 4
CANCELED = 5
STATUSES = (
    (REVIEW, 'На рассмотрении'),
    (READY, 'Готов к выдаче'),
    (RENTED, 'На выдаче'),
    (RETURNED, 'Возвращено'),
    (EXPIRED, 'Просрочено'),
    (CANCELED, 'Отменен')
)

TODAY = datetime.date.today()


class OrderManager(models.Manager):
    def expired_orders(self):
        """Проверка на просроченные заказы"""
        return super().get_queryset().filter(Q(archived=False) & Q(end_date__lt=TODAY))

    def cancel_waiting(self):
        """Выбор заказов готовых к выдаче с превышенным временем ожидания в 3 дня"""
        now = timezone.now() - datetime.timedelta(days=3)
        return super().get_queryset().filter(created__lt=now, status=1)


class Order(models.Model):
    """Заказ"""
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    books = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUSES, default=REVIEW)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    archived = models.BooleanField(default=False)

    objects = OrderManager()

    def __str__(self):
        return f'Заказ № {self.id}'

    def order_expired(self):
        """Изменение статуса заказа на 'Просрочено' """
        self.status = EXPIRED
        self.save()

    def order_cancel(self):
        """Изменение статуса заказа на 'Отменен' """
        self.status = CANCELED
        self.archived = True
        self.save()

    def save(self, *args, **kwargs):
        """
        Вычисление стоимости заказа в зависимости от срока аренды перед сохранением
        """
        self.price = ((self.end_date - self.start_date).days + 1) * sum([book['price'] for book in self.books])
        super(Order, self).save(*args, **kwargs)
