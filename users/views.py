from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('books:index')
    success_message = 'Поздравляем! Вы успешно зарегистрировались!'


class UserProfileView(TemplateView):
    template_name = 'users/profile.html'


class UserProfileSettings(UpdateView):
    model = User
    template_name = 'users/settings.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))




