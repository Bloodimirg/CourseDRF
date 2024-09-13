from rest_framework.decorators import action
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer, CourseWithCountSerializer,
)


# ----------------------------------------- ViewSet курсов
class CourseViewSet(ModelViewSet):
    """ViewSet для управления курсами. POST/GET/PUT(PATCH)/DELETE"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CourseSerializer  # Список курсов
        elif self.action == "retrieve":
            return CourseDetailSerializer  # Курс с количеством уроков и уроками
        elif self.action == "list_with_count":
            return CourseWithCountSerializer  # Курсы с количеством уроков
        return CourseSerializer

    @action(detail=False, methods=['get'])
    def list_with_count(self, request):
        """Эндпоинт для вывода курсов с количеством уроков"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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

