from rest_framework.serializers import ModelSerializer, SerializerMethodField

from config import settings
from materials.models import Course, Lesson, Subscription
from materials.validators import VideosValidator, HasLinkValidator


class LessonSerializer(ModelSerializer):
    validators = [
        VideosValidator(field="video_link")
    ]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField()
    validators = [
        HasLinkValidator(field="description"),
        HasLinkValidator(field="title"),
    ]

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "preview",
            "count_lessons",
            "lessons",
            "owner",
            "subscription",
        )

    def get_count_lessons(self, instance):
        obj = instance.lessons.all()
        if obj:
            return obj.count()
        return 0

    def get_subscription(self, instance):
        # user = self.request.user
        obj = instance.subscription_course.filter(owner=settings.AUTH_USER_MODEL)
        if obj:
            return True
        else:
            False


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

