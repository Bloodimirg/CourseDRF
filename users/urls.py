from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (
    PaymentCreateApiView,
    PaymentDestroyApiView,
    PaymentListApiView,
    PaymentRetrieveApiView,
    PaymentUpdateApiView, UserCreateApiView, CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('payment/', PaymentListApiView.as_view(), name='payment-list'),
    path('payment/<int:pk>/', PaymentRetrieveApiView.as_view(), name='payment-detail'),
    path('payment/create/', PaymentCreateApiView.as_view(), name='payment-create'),
    path('payment/<int:pk>/update/', PaymentUpdateApiView.as_view(), name='payment-update'),
    path('payment/<int:pk>/delete/', PaymentDestroyApiView.as_view(), name='payment-delete'),

    path('register/', UserCreateApiView.as_view(permission_classes=(AllowAny,)), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
