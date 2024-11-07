from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response

from utils.viewsets import OrderedModelViewSet

from .models import EditorModel
from .serializers import EditorModelSerializer


class EditorModelViewset(OrderedModelViewSet):
    queryset = EditorModel.objects.all()
    serializer_class = EditorModelSerializer
    filter_backends = []

    def get_object(self):
        lookup_value = self.kwargs[self.lookup_url_kwarg or self.lookup_field]
        filter_kwargs = (
            {"is_active": True}
            if lookup_value == "active"
            else {self.lookup_field: lookup_value}
        )
        return get_object_or_404(self.get_queryset(), **filter_kwargs)

    def get_serializer_data(self, request, obj):
        obj["user"] = request.user.pk
        return super().get_serializer_data(request, obj)
