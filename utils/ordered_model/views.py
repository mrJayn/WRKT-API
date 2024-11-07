from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from utils.viewsets import DynamicFieldsModelViewset


class OrderedModelViewSet(DynamicFieldsModelViewset):
    """
    A `ModelViewSet` which provides the default `list()`, `create()`,
    `partial_update()` and `destroy()` actions. Also provides the custom
    `create_obj()` method which can used to modify the `request.data`.

    The serializer context includes the ordered_queryset's `count` and
    `order_values` and the model class attr `MAX_COUNT`.

    ** REQUIRES that `serializer_class` is an `OrderedModelSerializer` subclass.
    """

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]

    def create(self, request, *args, **kwargs):
        """
        Method to create an ordered model instance.
        Handles the "order" field by default.
        """
        data = self.get_serializer_data(request, {})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = self.serializer_class(instance)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_serializer_data(self, request, obj):
        """
        Prepare the `data` arg for the serializer class. Default dict that includes a calculated value for the "order" key .
        """

        # set order field
        order = request.data.get("order", None)
        if not order:
            order = self.get_queryset().get_next_order()
        obj["order"] = order

        # set related fields
        # wrt_map = self.get_wrt_map()
        # if wrt_map is not None:
        #     for k,v in wrt_map.items():
        #         obj[k] = v

        return obj

    def get_wrt_map(self):
        queryset = self.get_queryset()
        if queryset.exists():
            return queryset.first()._wrt_map(serialize=True)
        return None
