from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from celery import shared_task

from users.models import User
from materials.services import send_telegram_message


@shared_task
def send_update_lesson_email(message, subject, recipient_email):
    send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_email)
    users = User.objects.get(email__in=recipient_email)
    if users:
        for user in users:
            if user.telegram_id:
                send_telegram_message(chat_id=user.telegram_id, message=message)


@shared_task
def check_last_login():
    today = timezone.now().today().date()
    users = User.objects.filter(last_login__isnull=False, last_login__lt=today - timezone.timedelta(days=30))
    if users:
        for user in users:
            user.is_active = False
