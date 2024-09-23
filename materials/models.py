from django.db import models
from config import settings

NULLABLE = {"blank": True, "null": True}

class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=50, verbose_name="Название курса")
    image = models.ImageField(upload_to="materials/course", **NULLABLE)
    description = models.TextField(verbose_name="Описание курса", help_text="Введите описание курса", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор', help_text='Укажите автора')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        permissions = [
            ('can_view_course', 'Может просматривать курсы'),
            ('can_edit_course', 'Может редактировать курсы'),
        ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(max_length=50, verbose_name="Название урока")
    image = models.ImageField(upload_to="materials/lesson", **NULLABLE)
    description = models.TextField(verbose_name="Описание урока", help_text="Введите описание урока", **NULLABLE)
    video_url = models.URLField(**NULLABLE, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Название курса", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор урока")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        permissions = [
            ('can_view_lesson', 'Может просматривать уроки'),
            ('can_edit_lesson', 'Может редактировать уроки'),
        ]

    def __str__(self):
        return self.title

class Subscription(models.Model):
    """Модель подписки"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} - {self.course}"
