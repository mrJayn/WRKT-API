from rest_framework import serializers
from utils.serializers import UserModelSerializer, OrderedUserModelSerializer

'''
class RelatedLibraryExerciseSerializer(UserModelSerializer):
    class Meta:
        model: LibraryExercise


class SetSerializer(OrderedUserModelSerializer):
    """A ModelSerializer for model instances of the `ExerciseSet` model class."""

    class Meta:
        model = ExerciseSet
        fields = [
            "id",
            "exercise",
            "sets",
            "reps",
            "weight",
            "percent",
            "calculated_weight",
        ]


class ExerciseSerializer(OrderedUserModelSerializer):
    """A ModelSerializer for model instances of the `Exercise` model class."""

    sets = SetSerializer(
        many=True,
        read_only=True,
    )
    # library_exercise = RelatedLibraryExerciseSerializer()

    class Meta:
        model = Exercise
        fields = [
            "id",
            "order",
            "day",
            "week",
            "name",
            # "library_exercise",
            "sets",
        ]
        # read_only_fields = ["sets", "library_exercise"]

    def create(self, validated_data):
        # Ensure that at least one of the Foreign Key fields has been provided.
        if validated_data.get("day", validated_data.get("week", None)) is None:
            raise serializers.ValidationError(
                "At least one related field must have a non-null value."
            )
        return super().create(validated_data)

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     library_exercise = ret.get("library_exercise",None)
    #     if isinstance(library_exercise,LibraryExercise):
    #         ret["library_exercise"] = library_exercise.pk
    #     return ret

    # def check_wrt_fields(self, validated_data):
    #     """Ensure that at least one of the Foreign Key fields has been provided."""
    #     wrt_field_names = self.context.get("wrt_field_names", None)
    #     for field in wrt_field_names:
    #         if validated_data.get(field, None) is not None:
    #             return
    #     raise serializers.ValidationError(
    #         "At least one related field must have a non-null value."
    #     )
'''
