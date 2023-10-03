from rest_framework.permissions import (BasePermission, IsAuthenticated,
                                        SAFE_METHODS)


class IsOwnerOrReadOnly(BasePermission):
    """Перминш для моделей Review."""
    def has_permission(self, request, view):
        """GET-запрос не требует авторизации."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Пользователь User не может редактировать(удлять) чужой объект."""
        return (
            request.method in SAFE_METHODS or obj.user == request.user
        )


class UserDeletePermission(IsAuthenticated):
    """
    Пользователь может удалить только свой аккаунт.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
