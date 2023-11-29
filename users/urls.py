from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from books.views import BooksListView
from users.views import UserRegistrationView, UserLoginView, UserProfileView, UserProfileSettings, \
    EmailVerificationView, send_email_verification

app_name = 'users'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name='login'),
    path("registration/", UserRegistrationView.as_view(), name='registration'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("profile/<int:pk>", login_required(UserProfileView.as_view()), name='profile'),
    path("profile/<int:pk>/settings", login_required(UserProfileSettings.as_view()), name='settings'),
    path("verify/<str:email>/<uuid:code>", EmailVerificationView.as_view(), name='email_verification'),
    path("send_verify/", send_email_verification, name='send_email_verification')
]
