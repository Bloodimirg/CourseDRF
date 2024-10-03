from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView, get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer, SubscriptionSerializer,
)
from materials.tasks import mailing
from users.permissions import IsModerator, IsOwner


# ----------------------------------------- ViewSet курсов
class CourseViewSet(ModelViewSet):
    """ViewSet для управления курсами. POST/GET/PUT(PATCH)/DELETE"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        # рассылка когда курс обновился
        serializer.save()
        course_pk = self.get_object().pk
        mailing.delay(course_pk)

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
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class LessonListApiView(ListAPIView):
    """Получение списка всех уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsModerator)
    pagination_class = CustomPagination

    # фильтрация отображения списка объектов только для модератора или владельца объекта
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)

class LessonRetrieveApiView(RetrieveAPIView):
    """Получение деталей конкретного урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)

class LessonUpdateApiView(UpdateAPIView):
    """Изменение существующего урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)

class LessonDestroyApiView(DestroyAPIView):
    """Удаление существующего урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)

class SubscriptionViewSet(APIView):
    """Подписка на курс"""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course = get_object_or_404(Course, pk=course_id)
        sub_item = Subscription.objects.all().filter(user=user).filter(course=course)

        if sub_item.exists():
            sub_item.delete()
            message = "Подписка отключена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка включена"
        return Response({"message": message})

