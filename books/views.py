from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, TemplateView

from books.models import Basket, Book, Category
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    """Стартовая страница"""
    template_name = 'books/index.html'
    title = 'Library Book'


class BookDetailView(TitleMixin, DetailView):
    """Подробное описание книги"""
    model = Book
    context_object_name = 'book'
    title = 'Library Book'
    template_name = 'books/book.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data()
        book = context['book']
        if book.liked_by.filter(id=self.request.user.id):
            context['is_liked'] = True
        else:
            context['is_liked'] = False
        return context


class BooksListView(TitleMixin, ListView):
    """Каталог книг"""
    model = Book
    template_name = 'books/books.html'
    title = 'Library - Каталог'

    def get_queryset(self):
        queryset = super(BooksListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BooksListView, self).get_context_data()
        categories = cache.get('categories')
        if not categories:
            context['categories'] = Category.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context


class BooksLikedList(TitleMixin, ListView):
    """Список избранных книг"""
    template_name = 'books/liked_books.html'
    title = 'Library - Избранное'

    def get_queryset(self):
        return self.request.user.liked_books.all()


@login_required
def add_like(request, book_id):
    book = Book.objects.get(id=book_id)
    book.add_like(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def remove_like(request, book_id):
    book = Book.objects.get(id=book_id)
    book.remove_like(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class BasketView(TitleMixin, TemplateView):
    """Корзина"""
    template_name = 'books/baskets.html'
    title = 'Library - Корзина'


@login_required
def basket_add(request, book_id):
    """
    Добавление товара в корзину
    :param request: используется для определения id пользователя
    :param book_id: id книги
    :return: Обновление страницы
    """
    book = Book.objects.get(id=book_id)
    baskets = Basket.objects.filter(user=request.user, book=book)

    if not baskets.exists():
        Basket.objects.create(user=request.user, book=book)
    else:
        print('Данная книга уже добавлена в корзину')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    """
    Удаление товара из корзины
    """
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
