from django.contrib import admin
from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)
    list_filter = ("id", "email")
