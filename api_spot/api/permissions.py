from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadOnly(BasePermission):
    """Перминш для моделей Review."""
    def has_permission(self, request, view):
        """GET-запрос не требует авторизации."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Пользователь User не может редактировать чужой пост."""
        return (
            request.method in SAFE_METHODS or obj.author == request.user
            or not request.user.is_user
        )
