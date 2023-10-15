import datetime

from django.db import models

from books.models import Basket
from users.models import User


class Order(models.Model):
    REVIEW = 0
    READY = 1
    RENTED = 2
    RETURNED = 3
    STATUSES = (
        (REVIEW, 'На рассмотрении'),
        (READY, 'Готов к выдаче'),
        (RENTED, 'На выдаче'),
        (RETURNED, 'Возвращено')
    )

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

    # @classmethod
    # def cost_calculation(cls, user):
    #     baskets = Basket.objects.filter(user=user)


