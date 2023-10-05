from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from users.models import User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Library - Авторизация'


class UserRegistrationView(TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = 'Library - Регистрация'
    success_url = reverse_lazy('books:index')
    success_message = 'Поздравляем! Вы успешно зарегистрировались!'


class UserProfileView(TitleMixin, TemplateView):
    template_name = 'users/profile.html'
    title = 'Library - Личный кабинет'


class UserProfileSettings(UpdateView):
    model = User
    template_name = 'users/settings.html'
    form_class = UserProfileForm
    title = 'Library - Параметры'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
