from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonDestroyApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView, SubscriptionViewSet,
)

app_name = MaterialsConfig.name


router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    # urls уроков
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"),
    path("lesson/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lesson_delete"),

    # url подписки
    path("subscription/", SubscriptionViewSet.as_view(), name="subscription"), # передать в POST course_id : 6
]

urlpatterns += router.urls
