from rest_framework import serializers
from utils.serializers import OrderedModelSerializer
from .models import EditorModel


class EditorModelSerializer(OrderedModelSerializer):
    class Meta:
        model = EditorModel
