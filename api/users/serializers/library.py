from utils.serializers import UserModelSerializer
from api.users.models import LibraryExercise


class LibraryExerciseSerializer(UserModelSerializer):
    """A ModelSerializer for model instances of the `LibraryExercise` model class."""

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
        extra_kwargs = {
            "profile": {"write_only": True},
        }
