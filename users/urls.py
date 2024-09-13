from django.urls import path
from users.views import (
    PaymentCreateApiView,
    PaymentDestroyApiView,
    PaymentListApiView,
    PaymentRetrieveApiView,
    PaymentUpdateApiView,
)

app_name = "users"

urlpatterns = [
    path('payment/', PaymentListApiView.as_view(), name='payment-list'),
    path('payment/<int:pk>/', PaymentRetrieveApiView.as_view(), name='payment-detail'),
    path('payment/create/', PaymentCreateApiView.as_view(), name='payment-create'),
    path('payment/<int:pk>/update/', PaymentUpdateApiView.as_view(), name='payment-update'),
    path('payment/<int:pk>/delete/', PaymentDestroyApiView.as_view(), name='payment-delete'),
]
