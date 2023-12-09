from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from order.tasks import send_mail_expired_orders_task
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User
from users.tasks import send_email_verification_task


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Library - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = 'Library - Регистрация'
    success_url = reverse_lazy('users:login')
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


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Library - Подтверждение электронной почты'
    template_name = 'users/successful_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            # Добавить страницу с отклоненным подтверждением почты по причине истекшего срока действия ссылки
            return HttpResponseRedirect(reverse('index'))


@login_required
def send_email_verification(request):
    send_email_verification_task.delay(request.user.id)
    messages.success(request, 'Письмо с подтверждением отправлено на Ваш email!')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def send_email_expired(request):
    send_mail_expired_orders_task.delay()
    messages.success(request, 'Уведомления о просроченных заказах отправлены!')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
