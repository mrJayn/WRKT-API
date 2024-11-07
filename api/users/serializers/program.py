from utils.serializers import UserModelSerializer, OrderedUserModelSerializer
from api.users.models import Program, Week


class WeekSerializer(UserModelSerializer):
    """A ModelSerializer for model instances of the `Week` model class."""

    # exercises = ExerciseSerializer(
    #     read_only=True, many=True, fields=["id", "name", "sets"]
    # )

    class Meta:
        model = Week
        fields = [
            "id",
            "program",
            "week_id",
            # "exercises",
        ]


class ProgramSerializer(OrderedUserModelSerializer):
    """A ModelSerializer for model instances of the `Program` model class."""

    weeks = WeekSerializer(
        read_only=True,
        many=True,
        fields=["id", "name"],
    )

    class Meta:
        model = Program
        fields = [
            "id",
            "profile",
            "name",
            "startdate",
            "duration",
            "order",
            "is_active",
            "weeks",
        ]
