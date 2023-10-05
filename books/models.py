from django.db import models

# Create your models here.
from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    biography = models.TextField()

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    description = models.TextField()
    pages = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    copies = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book_images')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum([basket.book.price for basket in self])

    def quantity(self):
        return len(self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Книга: {self.book.title}'
