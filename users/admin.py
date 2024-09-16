from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователя"""
    list_display = ("id", "email", "phone", "country", "get_groups")

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Groups'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Админка платежей"""
    list_display = ("id", "user", "date_payment", "lesson_paid", "course_paid", "amount", "payment_type")

