import os
from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models

# Create your models here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    # image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.first_name}'
        from_email = settings.EMAIL_HOST_USER
        to = self.user.email

        context = {'user': self.user, 'link': verification_link}
        html_content = render_to_string('users/email_verification.html', context=context).strip()

        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'

        image = 'email.png'

        img_path = os.path.join(settings.BASE_DIR, 'static/img/email.png')

        with open(img_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<{}>'.format(image))
            img.add_header('Content-Disposition', 'inline', filename=image)
            msg.attach(img)
        msg.send()


def is_expired(self):
    return True if now() >= self.expiration else False
