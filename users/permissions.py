from rest_framework import permissions


class IsOwmer(permissions.BasePermission):
    """Проверяет, является ли пользователь создателем."""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
