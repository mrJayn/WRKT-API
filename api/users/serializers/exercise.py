from rest_framework import serializers
from utils.serializers import OrderedModelSerializer, DynamicFieldsSerializer
from api.users.models import Exercise, SecondaryExercise, ExerciseSet, LibraryExercise


class SecondarySerializer(DynamicFieldsSerializer):
    class Meta:
        model = SecondaryExercise
        fields = [
            "exercise",
            "name",
            "sets",
            "reps",
            "weight",
            "percent",
            "calculated_weight",
            "units",
        ]
        # extra_kwargs = {"exercise": {"write_only": True}}


# =====


class SetSerializer(OrderedModelSerializer):
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
        # extra_kwargs = {"exercise": {"write_only": True}}


# =====


class ExerciseSerializer(OrderedModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if "library_ref" in ret and ret["library_ref"] is not None:
            ret["library_ref"] = ret["library_ref"].pk
        return ret

    class Meta:
        model = Exercise
        fields = ["id", "day", "week", "name", "order", "library_ref"]
        # extra_kwargs = {"day": {"write_only": True}, "week": {"write_only": True}}

    def check_wrt_fields(self, validated_data):
        """Checks if at least one related field is not None."""
        wrt_field_names = self.context.get("wrt_field_names", None)
        for field in wrt_field_names:
            if validated_data.get(field, None) is not None:
                return
        raise serializers.ValidationError(
            "At least one related field must have a non-null value."
        )

    def create(self, validated_data):
        self.check_wrt_fields(validated_data)
        return super().create(validated_data)


# =====


class WorkoutExerciseSerializer(OrderedModelSerializer):
    sets = SetSerializer(
        many=True,
        read_only=True,
        fields=["id", "sets", "reps", "weight"],
    )
    secondary = SecondarySerializer(
        read_only=True, fields=["name", "sets", "reps", "weight"]
    )

    class Meta:
        model = Exercise
        fields = ["id", "name", "order", "sets", "secondary"]
        read_only_fields = ["sets", "secondary"]


# =====


class ProgramExerciseSerializer(OrderedModelSerializer):
    sets = SetSerializer(
        many=True,
        read_only=True,
        fields=["sets", "reps", "percent", "calculated_weight"],
    )
    secondary = SecondarySerializer(
        read_only=True, fields=["name", "sets", "reps", "percent", "calculated_weight"]
    )

    class Meta:
        model = Exercise
        fields = ["name", "order", "library_max", "sets", "secondary"]

    library_max = serializers.SerializerMethodField("get_library_max")

    def get_library_max(self, obj):
        fixed_name = str(obj.name).lower().replace(" ", "_")
        instance = LibraryExercise.objects.filter(name=fixed_name)
        if instance.exists():
            return instance.max
        return None
