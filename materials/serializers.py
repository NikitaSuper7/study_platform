from rest_framework.serializers import ModelSerializer, SerializerMethodField

from config import settings
from materials.models import Course, Lesson, Subscription
from materials.validators import VideosValidator, HasLinkValidator
from users.services import convert_price


class LessonSerializer(ModelSerializer):
    validators = [VideosValidator(field="video_link")]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField()
    # usd_price = SerializerMethodField()
    validators = [
        HasLinkValidator(field="description"),
        HasLinkValidator(field="title"),
    ]

    class Meta:
        model = Course
        fields = ("id",
            "title",
            "description",
            "preview",
            "count_lessons",
            "lessons",
            "owner",
            "subscription",
            "price",
        )

    def get_count_lessons(self, instance):
        obj = instance.lessons.all()
        if obj:
            return obj.count()
        return 0

    def get_subscription(self, instance):
        request = self.context.get("request")
        user = request.user
        obj = instance.subscription_course.filter(owner=user)
        if obj:
            return True
        else:
            False

    # def get_usd_price(self, instance): # instance здесь это объект модели
    #     return convert_price(instance.amount)


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
