import datetime
import io
import os
from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from PIL import Image


def compressing_img(img_path, img_name):
    """Сжатие изображения (требуется для отправки email без вложения"""
    image = Image.open(img_path)
    quality = 95
    target = 15000
    minimum_quality = 50
    fixed_width = 200
    width, height = image.size
    image.thumbnail(size=(fixed_width, height))
    while True:
        output_buffer = io.BytesIO()
        image.save(output_buffer, "JPEG", quality=quality)
        file_size = output_buffer.tell()
        if file_size <= target or quality <= minimum_quality:
            output_buffer.close()
            break
        else:
            quality -= 5
    url = os.path.join(settings.BASE_DIR, 'media/book_images/compression', f'{img_name}.jpeg')
    image.save(url, "JPEG", quality=quality)
    return url


#  ====== НЕ ИСОЛЬЗУЕТСЯ
# Не используется (не знаю что лучше: функция или класс)
# class MimeImage:
#     def __init__(self, image, path_img, msg):
#         self.image = image
#         self.path_img = path_img
#         self.msg = msg
#
#     def set_name_content_id(self, value=1):
#         self.image = f'{self.image}_{value}'
#
#     def set_image_context(self):
#         with open(self.path_img, 'rb') as f:
#             img = MIMEImage(f.read())
#             img.add_header('Content-ID', self.image)
#             img.add_header('Content-Disposition', 'attachment', filename=self.image)
#             img.add_header("Content-Transfer-Encoding", "base64")
#             self.msg.attach(img)
# ======


def add_image_context(path_img, msg, context_key='image', image_id=None):
    """Добавление изображения в context"""
    if image_id:
        context_key = f'{str(context_key)}_{str(image_id)}'

    with open(path_img, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', context_key)
        img.add_header('Content-Disposition', 'attachment', filename=context_key)
        img.add_header("Content-Transfer-Encoding", "base64")
        msg.attach(img)


def custom_send_mail(
        subject_template_name,
        email_template_name,
        to_email,
        context,
        ):
    """
    Отправка email сообщения
    """
    domain = settings.DOMAIN_NAME
    login = reverse('users:login')
    books = reverse('books:index')
    links = {
        'index': domain,
        'login': f'{domain}{login}',
        'books': f'{domain}{books}',
    }
    context['links'] = links
    html_content = render_to_string(email_template_name, context=context).strip()

    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject_template_name, html_content, from_email, to_email)
    msg.content_subtype = 'html'
    msg.mixed_subtype = 'multipart'

    for order in context['orders']:
        for book in order.books:
            img_path = os.path.join(settings.BASE_DIR, book.get('image')[1:])
            new_path = compressing_img(img_path, f'image_{book.get("book_id")}')
            add_image_context(new_path, msg, image_id=book.get('book_id'))
            os.remove(new_path)

    logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo_for_email.png')
    add_image_context(logo_path, msg, context_key='logo_for_email')

    return msg


def send_expired_email(user, orders):
    """Отправка сообщения с просроченными заказами"""
    expired_days = datetime.date.today() - orders.first().end_date
    context = {'user': user, 'orders': orders, 'expired_days': expired_days.days}
    msg = custom_send_mail(
        'ВНИМАНИЕ!!! У Вас есть просроченные заказы',
        'order/email_expired.html',
        [user.email],
        context)

    msg.send()


def send_email_about_cancel_order(user, orders):
    """Отправка сообщения с отмененными заказами"""
    context = {'user': user, 'orders': orders}
    msg = custom_send_mail(
        'Срок ожидания заказа истек!',
        'order/email_cancel_order.html',
        [user.email],
        context)

    msg.send()
