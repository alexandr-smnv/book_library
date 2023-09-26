from django.urls import path

from books.views import BooksListView

app_name = 'books'

urlpatterns = [
    path("", BooksListView.as_view(), name='index'),
    path("category/<int:category_id>", BooksListView.as_view(), name='categories'),
]
