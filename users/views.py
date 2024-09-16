from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserCreateApiView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCreateApiView(CreateAPIView):
    """Создание платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateApiView(UpdateAPIView):
    """Изменение платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentListApiView(ListAPIView):
    """Список платежей"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'date_payment': ['exact', 'gte', 'lte'],  # Фильтрация по дате (равно, больше или равно, меньше или равно)
        'course_paid': ['exact'],  # Фильтрация по курсу
        'payment_type': ['exact', 'icontains'],  # Фильтрация по типу оплаты (точное совпадение или подстрока)
    }
    ordering_fields = ['date_payment', 'payment_type']  # Поля для сортировки
    ordering = ['date_payment']


class PaymentRetrieveApiView(RetrieveAPIView):
    """Детали платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyApiView(DestroyAPIView):
    """Удаление платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
