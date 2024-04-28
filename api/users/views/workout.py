from rest_framework.decorators import action
from rest_framework.response import Response
from utils.viewsets import OrderedModelViewSet, DynamicFieldsModelViewset
from api.users.models import Workout, Day
from api.users.serializers import WorkoutSerializer, DaySerializer


class WorkoutViewset(OrderedModelViewSet):
    """
    A viewset for the `Workout` model that can
    list, update, create, and remove instances.
    """

    serializer_class = WorkoutSerializer
    exclude_fields = ["days"]

    def get_queryset(self):
        return self.request.user.profile.workouts.all()

    def create_obj(self, request, obj):
        obj["profile"] = request.user.profile.pk
        return super().create_obj(request, obj)


class DayViewset(DynamicFieldsModelViewset):
    """
    A viewset for the `Day` model that can
    list and update instances.
    """

    serializer_class = DaySerializer
    http_method_names = ["get", "patch"]
    exclude_fields = ["exercises"]
    filterset_fields = ["workout"]

    def get_queryset(self):
        return Day.objects.filter(workout__profile=self.request.user.profile)

    @action(
        detail=False,
        methods=["get"],
        url_path="active",
        fields="__all__",
    )
    def get_active_workout_days(self, request, pk=None):
        queryset = self.get_queryset().filter(workout__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
