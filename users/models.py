from django.db import models
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson


# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="email", help_text="Укажите почту"
    )
    phone_number = models.CharField(
        max_length=35,
        blank=True,
        verbose_name="phone_number",
        help_text="Укажите телефон",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="avatar",
        help_text="Загрузите автар.",
    )

    def __str__(self):
        return f"{self.email}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payments(models.Model):
    CASH = "Cash"
    SEND_TO_COUNT = "Send_to_count"

    STATE_CHOICES = [
        (CASH, "Наличные"),
        (SEND_TO_COUNT, "перевод на счет"),
    ]
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users",
        blank=True,
        null=True,
    )
    payment_date = models.DateField(
        auto_now_add=True, verbose_name="Дата оплаты", null=True, blank=True
    )
    purchased_lessons = models.ForeignKey(
        Lesson, blank=True, null=True, on_delete=models.CASCADE, related_name="lessons"
    )
    purchased_courses = models.ForeignKey(
        Course, blank=True, null=True, on_delete=models.CASCADE, related_name="courses"
    )
    amount = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_type = models.CharField(
        max_length=20, choices=STATE_CHOICES, verbose_name="Тип оплаты"
    )
