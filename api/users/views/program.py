from utils.viewsets import OrderedModelViewSet, DynamicFieldsModelViewset
from api.users.models import Week
from api.users.serializers import ProgramSerializer, WeekSerializer


class ProgramViewset(OrderedModelViewSet):
    """
    A viewset for the `Program` model that can
    list, update, create, and remove instances.
    """

    serializer_class = ProgramSerializer
    create_fields = ["name", "startdate", "duration"]

    def get_queryset(self):
        return self.request.user.profile.programs.all()

    def get_serializer_data(self, request, obj):
        obj["profile"] = request.user.profile.pk
        return super().get_serializer_data(request, obj)


class WeekViewset(DynamicFieldsModelViewset):
    """
    A viewset for the `Week` model that can only list instances.
    """

    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return self.queryset.filter(program__profile=self.request.user.profile)
