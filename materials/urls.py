from rest_framework.routers import SimpleRouter
from materials.views import (
    CourseViewSet,
    LessonListaApiView,
    LessonCreateApiView,
    LessonDestroyApiView,
    LessonUpdateApiView,
    LessonRetrieveApiView,
    SubscriptionApiView,
)
from materials.apps import MaterialsConfig
from django.urls import path


app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListaApiView.as_view(), name="lessons_list"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lesson_destroy",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("subscription/", SubscriptionApiView.as_view(), name="subscription"),
]

urlpatterns += router.urls
