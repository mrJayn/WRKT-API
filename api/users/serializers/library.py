from utils.serializers import DynamicFieldsSerializer
from api.users.models import LibraryExercise


class LibraryExerciseSerializer(DynamicFieldsSerializer):
    class Meta:
        model = LibraryExercise
        fields = [
            "profile",
            "id",
            "name",
            "bodypart",
            "equipment",
            "max",
            "enabled",
            "custom",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"profile": {"write_only": True}}
