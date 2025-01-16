from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from celery import shared_task

from users.models import User


@shared_task
def send_update_lesson_email(message, subject, recipient_email):
    send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_email)


@shared_task
def check_last_login():
    today = timezone.now().today().date()
    users = User.objects.filter(last_login__isnull=False, last_login__date_lt=today - timezone.timedelta(days=30))
    for user in users:
        user.is_active = False
