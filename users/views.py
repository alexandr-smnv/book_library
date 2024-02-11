from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (LoginView, PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from order.tasks import (send_mail_cancel_order_task,
                         send_mail_expired_orders_task)
from users.forms import (UserForgotPasswordForm, UserLoginForm,
                         UserProfileForm, UserRegistrationForm,
                         UserSetNewPasswordForm)
from users.models import EmailVerification, User
from users.tasks import send_email_verification_task


class UserLoginView(TitleMixin, LoginView):
    """Авторизация пользователя"""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Library - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = 'Library - Регистрация'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегистрировались!'


class UserProfileView(TitleMixin, TemplateView):
    """Личный кабинет пользователя"""
    template_name = 'users/profile.html'
    title = 'Library - Личный кабинет'


class UserProfileSettings(TitleMixin, SuccessMessageMixin, UpdateView):
    """Параметры пользователя"""
    model = User
    template_name = 'users/settings.html'
    form_class = UserProfileForm
    title = 'Library - Параметры'
    success_message = 'Данные успешно изменены!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView, SuccessMessageMixin):
    """Верификация пользователя"""
    title = 'Library - Подтверждение электронной почты'
    template_name = 'users/successful_verification.html'
    success_message = 'Поздравляем! Ваша учетная запись успешно подтверждена!'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        # Если верификация верна и срок кода подтверждения не истек
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            messages.add_message(self.request, messages.ERROR, 'Произошла ошибка. Срок действия ссылки истек. Пройдите '
                                                               'заново подтверждение почты в профиле пользователя!')
            return HttpResponseRedirect(reverse('books:index'))


@login_required
def send_email_verification(request):
    """Отправка письма с верификацией"""
    send_email_verification_task.delay(request.user.id)
    messages.success(request, 'Письмо с подтверждением отправлено на Ваш email!')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """Сброс пароля"""
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('books:index')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/mail__password_subject_reset_mail.txt'
    email_template_name = 'users/mail__password_reset_mail.html'
    html_email_template_name = 'users/mail__html_password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Установка нового пароля"""
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('books:index')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


# ДЛЯ ТЕСТА ОТПРАВКИ EMAIL
@login_required
def send_email_expired(request):
    """Отправка письма с просроченными заказами"""
    send_mail_expired_orders_task.delay()
    messages.success(request, 'Уведомления о просроченных заказах отправлены!')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def send_email_cancel_order(request):
    """Отправка письма об отмене заказа"""
    send_mail_cancel_order_task.delay()
    messages.success(request, 'Уведомления об отмене заказа отправлено!')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
