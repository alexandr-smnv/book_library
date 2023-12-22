import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from order.utils import add_image_context


class User(AbstractUser):
    # image = models.ImageField(upload_to='users_images', null=True, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("Пользователь с таким email уже существует"),
        },
        blank=True)

    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        domain = settings.DOMAIN_NAME
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        login = reverse('users:login')
        books = reverse('books:index')
        links = {
            'index': domain,
            'login': f'{domain}{login}',
            'books': f'{domain}{books}',
            'verification_link': f'{domain}{link}'
        }
        subject = f'Подтверждение учетной записи для {self.user.first_name}'
        from_email = settings.EMAIL_HOST_USER
        to = self.user.email

        context = {'user': self.user, 'links': links}
        html_content = render_to_string('users/mail__email_verification.html', context=context).strip()

        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'

        img_path = os.path.join(settings.BASE_DIR, 'static/img/email.png')
        logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo_for_email.png')
        add_image_context(logo_path, msg, context_key='logo_for_email')
        add_image_context(img_path, msg, context_key='email')
        msg.send()

    def is_expired(self):
        return True if now() >= self.expiration else False
