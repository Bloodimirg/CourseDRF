from django.db import models

from users.models import NULLABLE


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(max_length=50, verbose_name="Название урока")
    image = models.ImageField(upload_to="materials/lesson", **NULLABLE)
    description = models.TextField(
        verbose_name="Описание урока", help_text="Введите описание урока", **NULLABLE
    )
    video_url = models.URLField(**NULLABLE, verbose_name="Ссылка на видео")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=50, verbose_name="Название курса")
    image = models.ImageField(upload_to="materials/course", **NULLABLE)
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса", **NULLABLE
    )
    lesson = models.ForeignKey(
        Lesson, **NULLABLE, verbose_name="Уроки", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title
