from django.utils import timezone

from django.core.management import BaseCommand

from materials.models import Lesson, Course
from users.models import Payment, User


class Command(BaseCommand):
    """Наполнение БД для модели Payment"""

    def handle(self, *args, **options):
        # Получаем пользователя по email который уже есть в БД
        try:
            user = User.objects.get(email='user@mail.ru')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь с email user@mail.ru не найден'))
            return

        lesson = Lesson.objects.first()
        course = Course.objects.first()

        if not lesson or not course:
            self.stdout.write(self.style.ERROR('Не удалось найти урок или курс для оплаты'))
            return

        payment = Payment.objects.create(
            user=user,
            date_payment=timezone.now(),
            lesson_paid=lesson,
            course_paid=course,
            amount=500,
            payment_type='Наличные'
        )

        self.stdout.write(self.style.SUCCESS(f'Добавлена запись оплаты: {payment}'))
