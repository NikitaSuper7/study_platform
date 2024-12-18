from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="title", help_text="Введите название курса"
    )
    description = models.TextField(
        verbose_name="description", help_text="Введите описание", blank=True, null=True
    )
    preview = models.ImageField(upload_to="materials/courses", blank=True, null=True)

    def __str__(self):
        return f"course - {self.title}"

    class Meta:
        verbose_name = "курсы"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="title", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="description", help_text="Введите описание", blank=True, null=True
    )
    preview = models.ImageField(
        upload_to="materials/lessons",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    video_link = models.TextField(
        verbose_name="video_link",
        help_text="Добавьте ссылку на видео",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", null=True, blank=True
    )

    def __str__(self):
        return f"lesson - {self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
