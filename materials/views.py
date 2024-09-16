from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
)


# ----------------------------------------- ViewSet курсов
class CourseViewSet(ModelViewSet):
    """ViewSet для управления курсами. POST/GET/PUT(PATCH)/DELETE"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# ----------------------------------------- Generics уроков
class LessonCreateApiView(CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateApiView(UpdateAPIView):
    """Изменение существующего урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListApiView(ListAPIView):
    """Получение списка всех уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveApiView(RetrieveAPIView):
    """Получение деталей конкретного урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyApiView(DestroyAPIView):
    """Удаление существующего урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

