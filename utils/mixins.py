from django.db.models import ForeignKey
from rest_framework import mixins
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


class PartialUpdateModelMixin:
    """A model mixin for partially updating an instance."""

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DynamicFieldsMixin:
    """
    A mixin that provides the  `fields` attribute and `get_serializer()` and `get_fields()` methods.\n
    Requires that the `serializer_class` is a `DynamicFieldsModelSerializer` subclass.
    """

    fields = None
    exclude_fields = None
    create_fields = None
    create_only_fields = None

    def get_serializer(self, *args, **kwargs):
        if "fields" not in kwargs:
            fields = self.get_serializer_fields()
            if fields is not None:
                kwargs["fields"] = fields
        if "exclude_fields" not in kwargs:
            exclude_fields = self.get_exclude_fields()
            if exclude_fields is not None:
                kwargs["exclude_fields"] = exclude_fields
        return super().get_serializer(*args, **kwargs)

    def get_serializer_fields(self):
        if self.action == "create":
            return self._create_fields()
        fields = self.get_fields() or []
        create_only_fields = self.get_create_only_fields()
        if self.action in ["update", "partial_update"] and create_only_fields:
            return list(set(fields) - set(create_only_fields))
        return fields

    def get_fields(self):
        return self.fields
        # return getattr(self, "%s_fields" % self.action, None) or self.fields

    def get_exclude_fields(self):
        return self.exclude_fields

    def get_create_fields(self):
        return self.create_fields

    def get_create_only_fields(self):
        return self.create_only_fields

    def _create_fields(self):
        """Checks `create_fields` for wrts and appends those fields accordingly."""
        if issubclass(self.__class__, mixins.CreateModelMixin):
            create_fields = [
                *(self.get_create_fields() or []),
                *(self.get_create_only_fields() or []),
            ]
            # > required create fields
            for field in self.get_queryset().model._meta.concrete_fields:
                if isinstance(field, ForeignKey) and field.name not in create_fields:
                    create_fields.append(field.name)
            return create_fields


class ActionsMixin:
    def __init__(self, actions: list | tuple):
        if "create" in actions:
            self.create = mixins.CreateModelMixin.create
            self.perform_create = mixins.CreateModelMixin.perform_create
            self.get_success_headers = mixins.CreateModelMixin.get_success_headers

        if "retrieve" in actions:
            self.retrieve = mixins.RetrieveModelMixin.retrieve

        if "partial_update" in actions:
            self.partial_update = PartialUpdateModelMixin.partial_update

        if "update" in actions:
            self.destroy = mixins.UpdateModelMixin.update
            self.perform_update = mixins.UpdateModelMixin.perform_update
            self.partial_update = mixins.UpdateModelMixin.partial_update

        if "destroy" in actions:
            self.destroy = mixins.DestroyModelMixin.destroy
            self.perform_destroy = mixins.DestroyModelMixin.perform_destroy

        if "list" in actions:
            self.list = mixins.ListModelMixin.list


# ========== ========== ==========


MIXINS_MAP = {
    "create": mixins.CreateModelMixin,
    "retrieve": mixins.RetrieveModelMixin,
    "update": mixins.UpdateModelMixin,
    "partial_update": PartialUpdateModelMixin,
    "destroy": mixins.DestroyModelMixin,
    "list": mixins.ListModelMixin,
}


def as_mixins(actions: list | tuple):
    """
    Maps viewset action names to mixin classes.
    """
    mixins = []

    for name in list(actions):
        if name not in MIXINS_MAP:
            raise KeyError(
                "%s is not a viewset action name. Valid action names are: %s."
                % (name, ", ".join(MIXINS_MAP.keys()))
            )
        if name == "partial_update" and "update" in actions:
            continue
        mixins.append(MIXINS_MAP[name])

    return mixins
