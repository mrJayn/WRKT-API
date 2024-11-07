from rest_framework import permissions


class IsCurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.pk == user.pk


class IsCurrentUserOrAdminOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_staff  # admin
            or request.method in permissions.SAFE_METHODS  # read-only
            or (type(obj) == type(user) and obj == user)  # current user
        )
