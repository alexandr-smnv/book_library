import datetime

from django.db import models

from books.models import Basket
from users.models import User

REVIEW = 0
READY = 1
RENTED = 2
RETURNED = 3
EXPIRED = 4
STATUSES = (
    (REVIEW, 'На рассмотрении'),
    (READY, 'Готов к выдаче'),
    (RENTED, 'На выдаче'),
    (RETURNED, 'Возвращено'),
    (EXPIRED, 'Просрочено')
)


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    books = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUSES, default=REVIEW)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return f'Заказ № {self.id}'

    def save(self, *args, **kwargs):
        self.price = ((self.end_date - self.start_date).days + 1) * sum([book['price'] for book in self.books])
        super(Order, self).save(*args, **kwargs)
