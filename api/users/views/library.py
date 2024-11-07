from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


class IsCustomExercise(permissions.BasePermission):
    """Object-level permission to prevent the default LibraryExercises from being edited."""

    message = "Cannot edit the default library exercises."

    def has_object_permission(self, request, view, obj):
        return obj.custom == True


"""
1) library/ ..... all
2) library/<str:category>/ .... exercises list.
3) library/<str:category>/<int:exercise_id> .... exercises detail.
"""

'''
class LibraryExerciseViewset(viewsets.ModelViewSet):
    """
    A viewset for the `LibraryExercise` model that can
    list, update, create, and remove instances.
    """

    # serializer_class = LibraryExerciseSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    default_obj_editable_fields = ["max", "enabled"]
    max_custom_objs = 30

    def get_queryset(self):
        qs = self.request.user.profile.library.all()
        if self.action == "customs_list":
            return qs.filter(custom=True)
        if self.action == "defaults_list":
            return qs.filter(custom=False)
        return qs

    def get_serializer(self, *args, **kwargs):
        if self.action == "partial_update":
            if not self.get_object().custom:
                kwargs["fields"] = self.default_obj_editable_fields
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        if self.get_queryset().filter(custom=True).count() >= self.max_custom_objs:
            return Response(
                "Max count reached.({value})".format(value=self.max_custom_objs),
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = LibraryExercise.objects.create(
            profile=request.user.profile,
            **request.data,
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        filter_kwargs = {}
        if custom := self.request.query_params.get("custom"):
            if custom in ["True", "true", "False", "false"]:
                filter_kwargs["custom"] = custom in ["True", "true"]
        if bodypart := self.request.query_params.get("bodypart"):
            filter_kwargs["bodypart"] = bodypart
        if equipment := self.request.query_params.get("equipment"):
            filter_kwargs["equipment"] = equipment
        return queryset.filter(**filter_kwargs)

    # ===

    @action(detail=False, methods=["get"], url_path="default")
    def defualts_list(self, request):
        return super().list(request)

    @action(detail=False, methods=["get"], url_path="custom")
    def customs_list(self, request):
        return super().list(request)

'''
