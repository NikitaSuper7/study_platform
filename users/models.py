from django.db import models
from django.contrib.auth.models import AbstractUser


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
