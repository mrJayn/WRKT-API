from rest_framework import serializers
from utils.serializers import (
    UserModelSerializer,
    OrderedUserModelSerializer,
)
from api.users.models import Workout, Day


class DaySerializer(UserModelSerializer):
    """A ModelSerializer for model instances of the `Day` model class."""

    # exercises = ExerciseSerializer(
    #     read_only=True, many=True, fields=["id", "name", "sets"]
    # )

    class Meta:
        model = Day
        fields = [
            "id",
            "workout",
            "day_index",
            "name",
            # "exercises",
        ]

    # num_exercises = serializers.SerializerMethodField()
    # def get_num_exercises(self, obj):
    #     return obj.exercises.count()


class WorkoutSerializer(OrderedUserModelSerializer):
    """A ModelSerializer for model instances of the `Workout` model class."""

    # default_exclude_fields = ["days"]

    days = DaySerializer(many=True, read_only=True, exclude_fields=["workout"])

    class Meta:
        model = Workout
        fields = ["id", "profile", "name", "is_active", "order", "days"]
