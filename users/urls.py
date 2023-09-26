from django.contrib.auth.views import LogoutView
from django.urls import path

from books.views import BooksListView
from users.views import UserRegistrationView, UserLoginView

app_name = 'users'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name='login'),
    path("registration/", UserRegistrationView.as_view(), name='registration'),
    path("logout/", LogoutView.as_view(), name='logout')
]