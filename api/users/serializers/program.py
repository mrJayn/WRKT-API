from utils.serializers import OrderedModelSerializer, DynamicFieldsSerializer
from api.users.models import Program, Week


class ProgramSerializer(OrderedModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"
        # ["profile", "name", "startdate", "duration", "order", "is_active"]


class WeekSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Week
        fields = "__all__"
        # ["week_id"]
