import decimal

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

    # вычисление стоимости аренды в день
    def price_on_day(self):
        return round(self.price * decimal.Decimal(0.05), 0)

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

    def de_json(self):
        basket_item = {
            'book_id': self.book.id,
            'book_title': self.book.title,
            'author': f'{self.book.author.name} {self.book.author.surname}',
            'image': self.book.image.url,
            'price': float(self.book.price_on_day()),
        }
        return basket_item

    # обновление количества книг в наличии
    # ПОФИКСИТЬ ЧТОБЫ НА КАЖДУЮ КНИГУ НЕ ОТПРАВЛЯЛСЯ ОТДЕЛЬНЫЙ ЗАПРОС В БАЗУ
    def reduction_quantity(self):
        book = Book.objects.get(id=self.book.id)
        book.copies -= 1
        book.save()
