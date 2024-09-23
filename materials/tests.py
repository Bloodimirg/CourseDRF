from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """Класс тестирования"""
    def setUp(self):
        """Заполнение базы данных тестовыми данными"""
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Курс 1", description="Первый курс")
        self.lesson = Lesson.objects.create(title="Урок 1", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест на просмотр одного урока"""
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тест на создание урока"""
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test",
            "video_url": "http://youtube.com",
            "description": "Test description",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест обновления урока"""
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Test update",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Test update")

    def test_lesson_list(self):
        """Тест на список уроков"""
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_delete(self):
        """Тест на удаление урока"""
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

class SubscriptionTestCase(APITestCase):
    """Тестирование подписки на курсы """
    def setUp(self):
        """Заполнение базы данных тестовыми данными"""
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Подписка", description="Подписка на курс")
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("materials:subscription")
        data = {
            "user": self.user.pk,
            "course_id": self.course.pk,
        }
        response = self.client.post(url, data)
        response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка отключена"})