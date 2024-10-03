from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежей"""
    class Meta:
        model = Payment
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    class Meta:
        model = User
        fields = ("id", "email", "phone", "country", "avatar", "password")

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Обновляем поле last_login
        user.last_login = timezone.now()
        user.save()

        return token

