from django.urls import path

from books.views import BooksListView, basket_add, basket_remove, BasketView, BookDetailView

app_name = 'books'

urlpatterns = [
    path("", BooksListView.as_view(), name='index'),
    path("book/<int:pk>/", BookDetailView.as_view(), name='book_detail'),
    path("category/<int:category_id>", BooksListView.as_view(), name='categories'),
    path("basket", BasketView.as_view(), name='basket'),
    path("baskets/add/<int:book_id>", basket_add, name='basket_add'),
    path("baskets/remove/<int:basket_id>", basket_remove, name='basket_remove'),
]
