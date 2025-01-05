from django.contrib import admin
from materials.models import Course, Lesson, Subscription

# Register your models here.


@admin.register(Course)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
    # search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)
    # list_filter = ("id", "email")
