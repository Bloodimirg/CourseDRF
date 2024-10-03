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
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, CustomTokenObtainPairSerializer
from users.services import create_stripe_price, create_stripe_sessions, create_stripe_product


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

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)  # Создается запись оплаты в БД
        product_id = create_stripe_product(payment)  # Создаем продукт в Stripe
        price = create_stripe_price(payment.amount, product_id)  # Создаем цену в Stripe
        session_id, payment_link = create_stripe_sessions(price)  # Создаем сессию оплаты в Stripe
        payment.session_id = session_id  # Сохраняем ID сессии оплаты в БД
        payment.payment_link = payment_link  # Сохраняем ссылку на оплату в БД
        payment.save()  # Сохраняем

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

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
