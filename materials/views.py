from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from users.permissions import IsModeratorsPermission, IsOwnerPermission


# Create your views here.


# Для курсов через ModelViewSet:



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # Владельцем автоматический становится пользователь, который создает объект:
    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    # Модератор не может удалять или создавать:
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModeratorsPermission,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModeratorsPermission | IsOwnerPermission,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModeratorsPermission | IsOwnerPermission,)

        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (IsModeratorsPermission | IsOwnerPermission, IsAuthenticated)
        return super().get_permissions()


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (IsModeratorsPermission | IsOwnerPermission, IsAuthenticated)
        return super().get_permissions()


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (IsOwnerPermission, IsAuthenticated)
        return super().get_permissions()
