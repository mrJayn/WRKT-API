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

    def create_obj(self, request, obj):
        obj["profile"] = request.user.profile.pk
        return super().create_obj(request, obj)


class WeekViewset(DynamicFieldsModelViewset):
    """
    A viewset for the `Week` model that can only list instances.
    """

    serializer_class = WeekSerializer
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return Week.objects.filter(program__profile=self.request.user.profile)
