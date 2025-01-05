from rest_framework import permissions


class IsModeratorsPermission(permissions.BasePermission):
    """Входит ли пользователь в группу модераторов."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwnerPermission(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
