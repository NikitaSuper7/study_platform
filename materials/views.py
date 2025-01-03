from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from materials.models import Course, Lesson, Subscription
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)

from users.permissions import IsModeratorsPermission, IsOwnerPermission
from materials.paginators import MaterialsPaginator


# Create your views here.


# Для курсов через ModelViewSet:


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPaginator

    # Владельцем автоматический становится пользователь, который создает объект:
    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    # Модератор не может удалять или создавать:
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModeratorsPermission,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModeratorsPermission | IsOwnerPermission,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModeratorsPermission | IsOwnerPermission,)

        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        # queryset.
        return queryset


# Для уроков через generics:
class LessonCreateApiView(CreateAPIView):
    """Создает уроки"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perfom_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        self.permission_classes = (~IsModeratorsPermission, IsAuthenticated)
        return super().get_permissions()


class LessonListaApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModeratorsPermission | IsOwnerPermission, IsAuthenticated)
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (
            IsModeratorsPermission | IsOwnerPermission,
            IsAuthenticated,
        )
        return super().get_permissions()


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (
            IsModeratorsPermission | IsOwnerPermission,
            IsAuthenticated,
        )
        return super().get_permissions()


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (IsOwnerPermission, IsAuthenticated)
        return super().get_permissions()


class SubscriptionApiView(APIView):
    serializer_class = SubscriptionSerializer
    # queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        # self.permission_classes = (AllowAny)
        user = self.request.user
        course_id = self.request.data.get("course")
        # course = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(owner=user, course_id=course_id)

        if subs_item.exists():
            sub = Subscription.objects.get(owner=user, course_id=course_id)
            sub.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(owner=user, course_id=course_id)
            message = "Подписка создана"
        return Response({"message": message})
