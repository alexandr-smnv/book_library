from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)

from users.models import User
from users.tasks import (send_email_verification_task,
                         send_mail_reset_password_task)


class UserLoginForm(AuthenticationForm):
    """Форма для авторизации пользователя"""
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите имя пользователя',
        }))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите пароль'
        }))


class UserRegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите имя'
        }))
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите фамилию'
        }))
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите имя пользователя'
        }))
    email = forms.CharField(
        label='Адрес электронной почты',
        widget=forms.EmailInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите адрес эл. почты'
        }))
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите пароль'
        }))
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Подтвердите пароль'
        }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """Сохранение пользователя"""
        user = super(UserRegistrationForm, self).save(commit=True)
        # создание таски на отправку письма для верификации
        send_email_verification_task.delay(user.id)
        return user


class UserProfileForm(forms.ModelForm):
    """Форма с параметрами пользователя"""
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4'
        }))
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4'
        }))
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
        }))
    email = forms.CharField(
        label='Адрес электронной почты',
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
        }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserForgotPasswordForm(PasswordResetForm):
    """Форма для сброса пароля"""
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    def send_mail(self,
                  subject_template_name,
                  email_template_name,
                  context,
                  from_email,
                  to_email,
                  html_email_template_name=None):
        """
            Переопределение метода send_mail (вызов celery task)
        """
        context['user'] = context['user'].id

        send_mail_reset_password_task.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name)


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Установка нового пароля
    """
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
