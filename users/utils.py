import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.urls import reverse

from order.utils import add_image_context


def send_email_reset_password(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
):

    domain = settings.DOMAIN_NAME
    login = reverse('users:login')
    books = reverse('books:index')
    link = reverse('users:password_reset_confirm', kwargs={
        'uidb64': context.get('uid'),
        'token': context.get('token')
    })
    links = {
        'index': f'{domain}',
        'login': f'{domain}{login}',
        'books': f'{domain}{books}',
        'reset_password': f'{domain}{link}',
    }
    context['links'] = links
    subject = loader.render_to_string(subject_template_name, context)

    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")
        img_path = os.path.join(settings.BASE_DIR, 'static/img/password_reset.png')
        logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo_for_email.png')
        add_image_context(logo_path, email_message, context_key='logo_for_email')
        add_image_context(img_path, email_message, context_key='password')

    email_message.send()
