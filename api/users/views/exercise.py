from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, Q

from django.utils.translation import gettext_lazy as _

import utils
from utils.mixins import DynamicFieldsMixin
from utils.viewsets import OrderedModelViewSet, DynamicFieldsModelViewset
from api.users.models import Exercise, SecondaryExercise, ExerciseSet
from api.users.serializers import ExerciseSerializer, SecondarySerializer, SetSerializer


class ExerciseViewset(OrderedModelViewSet):
    """
    A viewset for the `Exercise` model that can
    list, update, create, and remove instances.
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    # fields = ["name", "order"]
    create_only_fields = ["order"]
    lookup_field = "id"

    def get_queryset(self):
        profile = self.request.user.profile
        return self.queryset.filter(
            Q(day__workout__profile=profile) | Q(week__program__profile=profile)
        )

    # def get_queryset(self):
    #     return utils.query_exercise(self.request, **self.kwargs)

    def create_obj(self, request, obj):
        qs = self.get_queryset()
        active_wrt = "day" if "workout" in request.path else "week"
        if qs.exists():
            obj = {**obj, **qs.first()._wrt_map()}
        else:
            obj["day"] = utils.get_day_object(request, **self.kwargs)
            obj["week"] = utils.get_week_object(request, **self.kwargs)
        obj[active_wrt] = obj[active_wrt].pk
        return super().create_obj(request, obj)

    def get_fields(self):
        fields = self.fields
        if "workout" in self.request.path and fields:
            fields.append("library_ref")
        return fields

    @action(detail=False, methods=["get"], url_path="active")
    def get_active_workout_exercises(self, request, pk=None):
        queryset = self.get_queryset().filter(day__workout__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ---


class ExerciseChildMixin:
    def get_exercise(self):
        return utils.query_exercise(self.request, **self.kwargs)

    def get_fields(self):
        for_wkt = "workout" in self.request.path
        extra_fields = (
            ["weight"] if for_wkt else ["percent", "calculated_weight", "units"]
        )
        return [*self.fields, *extra_fields]


class SecondaryViewset(ExerciseChildMixin, DynamicFieldsModelViewset):
    queryset = SecondaryExercise.objects.all()
    serializer_class = SecondarySerializer
    fields = ["name", "sets", "reps"]

    def get_object(self):
        try:
            return SecondaryExercise.objects.get(exercise=self.get_exercise())
        except ObjectDoesNotExist:
            raise NotFound({})

    def create(self, request, *args, **kwargs):
        data = {"exercise": self.get_exercise().pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---


class SetsViewset(ExerciseChildMixin, OrderedModelViewSet):
    serializer_class = SetSerializer
    fields = ["sets", "reps"]

    def get_queryset(self):
        return ExerciseSet.objects.filter(exercise=self.get_exercise())

    def create_obj(self, request, obj):
        if "exercise" not in obj:
            obj["exercise"] = self.get_exercise().pk
        print(f"obj = {obj}")
        return super().create_obj(request, obj)
