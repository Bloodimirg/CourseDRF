from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Информация об уроках"""
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Стандартный вывод информации о курсах"""
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

class CourseWithCountSerializer(serializers.ModelSerializer):
    """Вывод курсов с количеством уроков"""
    count_lessons = serializers.SerializerMethodField()

    def get_count_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = ("id", "title", "description", "count_lessons")


class CourseDetailSerializer(serializers.ModelSerializer):
    """Вывод курсов с количеством уроков и информацией по всем урокам"""
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_count_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = ("id", "title", "description", "count_lessons", "lessons")
