from django.shortcuts import render
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer, PaymentsSerializer, PaymentsCreateSerializer

from users.models import User, Payments
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter

# Для создания пользователя
from rest_framework.generics import CreateAPIView

from users.services import convert_price, create_stripe_price, create_stripe_session


# Create your views here.


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Чтобы регистрироваться могли анонимные пользователи
    permission_classes = (AllowAny,)

    # Для того, чтобы пользователь создавался корректно:
    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class PaymentsListApiView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )  # Бэкенд для обработки фильтра
    filterset_fields = ("purchased_courses", "purchased_lessons", "payment_type")
    ordering_fields = ("payment_date",)

class PaymentsCreateApiView(CreateAPIView):
    serializer_class = PaymentsCreateSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(username=self.request.user)
        amount_in_dollars = convert_price(payment.purchased_courses.price)
        price = create_stripe_price(amount_in_dollars)
        session_id, payment_link = create_stripe_session(price)
        payment.link = payment_link
        payment.session_id = session_id
        payment.amount = payment.purchased_courses.price
        payment.save()
