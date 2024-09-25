from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_urls


class LessonSerializer(serializers.ModelSerializer):
    """Информация об уроках"""
    video_url = serializers.URLField(validators=[validate_urls])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Вывод информации о курсах"""
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True, required=False)
    count_lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_count_lessons(self, course):
        return course.lesson_set.count()

    def get_subscription(self, obj):
        # Получаем текущего пользователя из контекста запроса
        user = self.context['request'].user
        # Проверяем, существует ли подписка на данный курс
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "image",
            "description",
            "owner",
            "count_lessons",
            "subscription",
            "lessons",

        ]

class SubscriptionSerializer(serializers.ModelSerializer):
    """Подписка на курс"""
    class Meta:
        model = Subscription
        fields = "__all__"
