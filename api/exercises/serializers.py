from rest_framework import serializers

from .models import BaseExercise


class BaseExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseExercise
        fields = ["name", "bodypart", "equipment"]
        read_only_fields = ["name", "bodypart", "equipment"]
