from django.shortcuts import render
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer, PaymentsSerializer

from users.models import User, Payments
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter


# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentsListApiView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)  # Бэкенд для обработки фильтра
    filterset_fields = ('purchased_courses', 'purchased_lessons', 'payment_type')
    ordering_fields = ('payment_date',)
