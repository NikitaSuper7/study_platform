from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.models import Course, Lesson



class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ("title", "description", "preview", "count_lessons", "lessons")

    def get_count_lessons(self, instance):

        obj = instance.lessons.all()
        if obj:
            return obj.count()
        return 0



