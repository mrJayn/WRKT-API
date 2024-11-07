from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from api.users.models import Workout, Day
from api.users.serializers import WorkoutSerializer, DaySerializer
from utils.viewsets import DynamicFieldsModelViewset, OrderedModelViewSet

"""
Workout Creation

frontend_data = {
  "name": "New Workout {next_order}", 
  "num_days": 7 ( min:0 , max:14 )
}

auto_fields 
  "id"
  "profile"
  "is_active" - False if other workouts else True 
  "order" - next order 
"""


class WorkoutViewset(OrderedModelViewSet):
    """
    List, create, update, and delete instances of the `Workout` model.
    """

    serializer_class = WorkoutSerializer
    # exclude_fields = ["days"]

    def get_queryset(self):
        return self.request.user.profile.workouts.all()

    def get_object(self):
        lookup_value = self.kwargs[self.lookup_url_kwarg or self.lookup_field]
        filter_kwargs = (
            {"is_active": True}
            if lookup_value == "active"
            else {self.lookup_field: lookup_value}
        )
        return get_object_or_404(self.get_queryset(), **filter_kwargs)

    def get_serializer_data(self, request, obj):
        obj["profile"] = request.user.profile.pk
        return super().get_serializer_data(request, obj)

    # @action(
    #     detail=True,
    #     url_path="exercises",
    #     serializer_class=ExerciseSerializer,
    #     exclude_fields=["week"],
    # )
    # def exercises(self, request, pk=None):
    #     workout = self.get_object()
    #     exercises_qs = Exercise.objects.filter(day__workout=workout.pk)
    #     serializer = ExerciseSerializer(
    #         exercises_qs,
    #         many=True,
    #         exclude_fields=["week"],
    #     )
    #     return Response(serializer.data)


class DayViewset(DynamicFieldsModelViewset):
    """
    List and update instances of the `Day` model.
    """

    http_method_names = ["get", "patch"]
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    filterset_fields = ["workout"]

    def get_queryset(self):
        return self.queryset.filter(workout__profile=self.request.user.profile)

    @action(
        methods=["get"],
        detail=False,
        url_path="active",
        url_name="active",
        exclude_fields=None,
    )
    def get_active_workout_days(self, request, pk=None):
        queryset = self.get_queryset().filter(workout__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
