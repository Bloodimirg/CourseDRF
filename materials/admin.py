from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админка уроков"""
    list_display = ("pk", "title", "course", "description", "video_url")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка курсов"""
    list_display = ("pk", "title", "image", "description")
