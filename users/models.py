from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Lesson, Course

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone = models.CharField(max_length=40, **NULLABLE, verbose_name="Телефон (Не обязательно)")
    country = models.CharField(max_length=50, **NULLABLE, verbose_name="Страна (Не обязательно)")
    avatar = models.ImageField(upload_to="users/avatars", **NULLABLE, verbose_name="Аватар (Не обязательно)")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель платежей"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", **NULLABLE)
    date_payment = models.DateTimeField(verbose_name="Дата оплаты", auto_now_add=True)
    lesson_paid = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE)
    course_paid = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_type = models.CharField(max_length=50, verbose_name="Тип оплаты")


    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user.email} - {self.lesson_paid.title if self.lesson_paid else self.course_paid.title}"

