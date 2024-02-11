from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, UserForgotPasswordView,
                         UserLoginView, UserPasswordResetConfirmView,
                         UserProfileSettings, UserProfileView,
                         UserRegistrationView, send_email_cancel_order,
                         send_email_expired, send_email_verification)

app_name = 'users'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name='login'),
    path("registration/", UserRegistrationView.as_view(), name='registration'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("profile/<int:pk>", login_required(UserProfileView.as_view()), name='profile'),
    path("profile/<int:pk>/settings", login_required(UserProfileSettings.as_view()), name='settings'),
    path("verify/<str:email>/<uuid:code>", EmailVerificationView.as_view(), name='email_verification'),
    path("send_verify/", send_email_verification, name='send_email_verification'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # ДЛЯ ТЕСТА ОТПРАВКИ EMAIL
    path("send_expired/", send_email_expired, name='send_email_expired'),
    path("send_cancel/", send_email_cancel_order, name='send_email_cancel_order'),
]
