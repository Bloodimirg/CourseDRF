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

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator,) # создавать могут не модераторы
        elif self.action in ['update', 'retrieve', 'partial_update']:
            self.permission_classes = (IsModerator | IsOwner,) # обновлять может модератор или владелец
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator | IsOwner,) # удалять может не модератор или владелец
        return super().get_permissions()

    # Отображение списка объектов только если модератор, или владелец объектов
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)


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

