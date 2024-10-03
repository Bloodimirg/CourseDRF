from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course, Subscription
from users.models import User


@shared_task
def mailing(course_pk):
    """Рассылка если курс обновился"""
    email_list = []
    course = Course.objects.get(pk=course_pk)
    subs = Subscription.objects.filter(course=course)
    for sub in subs:
        email_list.append(sub.user.email)
    subject_mail = f'Обновление курса {course.title}'
    text_mail = f'Курс - {course.title} обновился.'
    send_mail(subject_mail, text_mail, settings.EMAIL_HOST_USER, email_list, fail_silently=True)
    print('Письмо отправлено')

@shared_task
def check_last_login():
    """Блокировка пользователя если не заходил 30 дней"""
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False, last_login__isnull=False)
    date_block = timezone.now() - timedelta(days=30)

    for user in users:
        if user.last_login <= date_block:
            print(f'Блокировка пользователя {user.email}')
            user.is_active = False
            user.save()

