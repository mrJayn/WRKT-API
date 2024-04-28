from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from django.db.models import ForeignKey
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
        if issubclass(self.__class__, CreateModelMixin):
            create_fields = [
                *(self.get_create_fields() or []),
                *(self.get_create_only_fields() or []),
            ]
            # > required create fields
            for field in self.get_queryset().model._meta.concrete_fields:
                if isinstance(field, ForeignKey) and field.name not in create_fields:
                    create_fields.append(field.name)
            return create_fields
