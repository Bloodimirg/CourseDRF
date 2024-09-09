from django.contrib import admin

from users.models import User


@admin.register(User)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "country")
