from rest_framework import serializers

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

