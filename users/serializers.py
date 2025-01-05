from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.models import User, Payments


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "is_staff", "is_active", "is_superuser")


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"

class PaymentsCreateSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
        read_only_fields = ("user",)
