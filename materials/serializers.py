from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_urls


class LessonSerializer(serializers.ModelSerializer):
    """Информация об уроках"""
    url_validator = serializers.URLField(validators=[validate_urls])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Вывод информации о курсах"""
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True, required=False)
    count_lessons = serializers.SerializerMethodField()

    def get_count_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "image",
            "description",
            "owner",
            "count_lessons",
            "lessons",
        ]

