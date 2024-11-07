from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response


from .models import BaseExercise
from .serializers import BaseExerciseSerializer


class IsAdminOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.method in SAFE_METHODS)


class BaseExerciseViewSet(viewsets.ModelViewSet):
    queryset = BaseExercise.objects.all()
    serializer_class = BaseExerciseSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "pk"
