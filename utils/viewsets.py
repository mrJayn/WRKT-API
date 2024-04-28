from typing import Any
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.utils.translation import gettext_lazy as _

from utils.mixins import DynamicFieldsMixin


class DynamicFieldsModelViewset(DynamicFieldsMixin, viewsets.ModelViewSet):
    pass


class OrderedModelViewSet(DynamicFieldsModelViewset):
    """
    A `ModelViewSet` which provides the default `list()`, `create()`,
    `partial_update()` and `destroy()` actions. Also provides the custom
    `create_obj()` method which can used to modify the `request.data`.

    The serializer context includes the ordered_queryset's `count` and
    `order_values` and the model class attr `MAX_COUNT`.

    ** REQUIRES that `serializer_class` is an `OrderedModelSerializer` subclass.
    """

    # lookup_field = "order"

    http_method_names = ["get", "post", "patch", "delete"]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        qs = self.get_queryset()
        context["order_values"] = list(qs.values_list("order", flat=True))
        context["qs_count"] = qs.count()
        return context

    def create(self, request, *args, **kwargs):
        # initial_data = self.get_related_wrt_map()
        data = self.create_obj(request, {})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = self.serializer_class(instance)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def create_obj(self, request, obj):
        """Modify the `obj` for the serializer to use as it's `data` kwarg ."""
        order = request.data.get("order", None)
        if not order:
            order = self.get_queryset().get_next_order()
        obj["order"] = order
        return obj

    @property
    def allowed_methods(self):
        allowed_methods = super().allowed_methods
        # Remove the POST method if the max-count has been reached.
        max_count = self.get_queryset().model.MAX_COUNT
        if max_count is not None and max_count <= self.get_queryset().count():
            return [i for i in allowed_methods if i != "POST"]
        return allowed_methods
