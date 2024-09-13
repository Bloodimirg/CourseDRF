from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователя"""
    list_display = ("id", "email", "phone", "country")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Админка платежей"""
    list_display = ("id", "user", "date_payment", "lesson_paid", "course_paid", "amount", "payment_type")

