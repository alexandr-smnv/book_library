from django.urls import path

from books.views import (BasketView, BookDetailView, BooksListView, basket_add,
                         basket_remove, add_like, remove_like, BooksLikedList)

app_name = 'books'

urlpatterns = [
    path("", BooksListView.as_view(), name='index'),
    path("category/<int:category_id>/", BooksListView.as_view(), name='categories'),
    path("book/<int:pk>/", BookDetailView.as_view(), name='book_detail'),
    path("liked_books/", BooksLikedList.as_view(), name='liked_books'),
    path("book/add_like/<int:book_id>/", add_like, name='add_like'),
    path("book/remove_like/<int:book_id>/", remove_like, name='remove_like'),
    path("basket/", BasketView.as_view(), name='basket'),
    path("baskets/add/<int:book_id>/", basket_add, name='basket_add'),
    path("baskets/remove/<int:basket_id>/", basket_remove, name='basket_remove'),
]
