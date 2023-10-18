from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from books.models import Book, Category, Basket
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'books/index.html'
    title = 'Library Book'


class BookDetailView(TitleMixin, DetailView):
    model = Book
    context_object_name = 'book'
    title = 'Library Book'
    template_name = 'books/book.html'


class BooksListView(TitleMixin, ListView):
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


class BasketView(TitleMixin, TemplateView):
    template_name = 'books/baskets.html'
    title = 'Library - Корзина'


@login_required
def basket_add(request, book_id):
    book = Book.objects.get(id=book_id)
    baskets = Basket.objects.filter(user=request.user, book=book)

    if not baskets.exists():
        Basket.objects.create(user=request.user, book=book)
    else:
        print('Данная книга уже добавлена в корзину')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
