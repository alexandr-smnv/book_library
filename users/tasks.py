import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User
from users.utils import send_email_reset_password


@shared_task()
def send_email_verification_task(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = EmailVerification.objects.get(user=user)
    if record:
        record.expiration = expiration
        record.save()
    else:
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()


@shared_task
def send_mail_for_reset_password(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
):

    context['user'] = User.objects.get(pk=context['user'])

    send_email_reset_password(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )
