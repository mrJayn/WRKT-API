from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from utils.viewsets import OrderedModelViewSet

from api.users.models import Day, Week

# from api.users.serializers import ExerciseSerializer, SetSerializer


class ExerciseViewset(OrderedModelViewSet):
    """
    A viewset for the `Exercise` model that can list, update, create, and remove instances.
    """

    # queryset = Exercise.objects.all()
    # serializer_class = ExerciseSerializer
    create_only_fields = ["order"]

    def get_queryset(self):
        if "day_pk" in self.kwargs:
            return self.queryset.filter(day=self.kwargs["day_pk"])
        if "week_pk" in self.kwargs:
            return self.queryset.filter(week=self.kwargs["week_pk"])
        # If no day or week is provided, return all exercises for the user.
        profile = self.request.user.profile
        return self.queryset.filter(
            Q(day__workout__profile=profile) | Q(week__program__profile=profile)
        )

    def get_serializer_data(self, request, obj):
        queryset = self.get_queryset()
        if queryset.exists():
            obj = {
                **obj,
                **queryset.first()._wrt_map(serialize=True),
            }
        if "day_pk" in self.kwargs:
            obj["day"] = Day.objects.get(pk=self.kwargs["day_pk"]).pk
        elif "week_pk" in self.kwargs:
            obj["week"] = Week.objects.get(pk=self.kwargs["week_pk"]).pk
        return super().get_serializer_data(request, obj)

    def get_exclude_fields(self):
        if "day_pk" in self.kwargs:
            return ["week"]
        if "week_pk" in self.kwargs:
            return ["day"]
        return None

    # @action(detail=False, methods=["get"], url_path="active")
    def get_active_workout_exercises(self, request, pk=None):
        queryset = self.get_queryset().filter(day__workout__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SetsViewset(OrderedModelViewSet):
    """
    List, create, update, and delete instances of the `ExerciseSet` model.
    """

    # queryset = ExerciseSet.objects.all()
    # serializer_class = SetSerializer
    fields = ["sets", "reps"]

    def get_queryset(self):
        exercise = self.get_exercise_object()
        return self.queryset.filter(exercise=exercise)

    def get_serializer_data(self, request, obj):
        if "exercise" not in obj:
            exercise = self.get_exercise_object()
            obj["exercise"] = exercise.pk
        return super().get_serializer_data(request, obj)

    def get_fields(self):
        if "day_pk" in self.kwargs:
            return [*self.fields, "weight"]
        elif "week_pk" in self.kwargs:
            return [*self.fields, "percent", "calculated_weight"]
        else:
            return self.fields

    def get_exercise_object(self):
        try:
            return None
            # return Exercise.objects.get(pk=self.kwargs["exercise_pk"])
        except:  # Exercise.DoesNotExist:
            return None


# class _DayExerciseViewset(ExerciseViewset):
#     serializer_class = ExerciseSerializer
#     exclude_fields = ["week"]


# class _DayExerciseSetDataViewset(OrderedModelViewSet):
#     serializer_class = SetSerializer
#     exclude_fields = ["exercise", "percent"]
