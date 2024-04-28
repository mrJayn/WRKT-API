from rest_framework import serializers
from utils.serializers import OrderedModelSerializer, DynamicFieldsSerializer
from api.users.models import Workout, Day
from .exercise import ExerciseSerializer


class DaySerializer(DynamicFieldsSerializer):
    exercises = ExerciseSerializer(read_only=True, many=True)

    class Meta:
        model = Day
        fields = ["id", "workout", "day_id", "name", "exercises"]


class WorkoutSerializer(OrderedModelSerializer):
    days = DaySerializer(read_only=True, many=True, fields=["name"])

    class Meta:
        model = Workout
        fields = ["id", "profile", "name", "is_active", "order", "days"]
