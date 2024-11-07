from copy import deepcopy
from django.db import models
from django.db.models import Model as DjangoModel
from django.utils.datastructures import ImmutableList
from django.utils.text import camel_case_to_spaces
from rest_framework import serializers
from .text import camel_to_snake, snake_to_camel


class CamelModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that converts keys to and from `camelCase`.

    _Example:_
    ~~~ py
        ...
        instance = { "is_active": True }
        serializer = CamelModelSerializer(instance)
        >> print(serializer.data) # { "isActive":True }

    ~~~
    """

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return {camel_to_snake(k): value.get(k) for k in value.keys()}

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        return {snake_to_camel(k): repr.get(k) for k in repr.keys()}


class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer to provide a serializer that takes either an additional `fields` or `exclude_fields`
    arguments that control which fields should or should not be displayed respectively.

    If neither the `fields` or `exlude_fields` arguments are provided, a default for `exclude_fields` can be set
    via the additional `default_exclude_fields` attribute. ( defaults to None )

    Modified from DRF's example:
    https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    """

    default_exclude_fields = None

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude_fields = kwargs.pop("exclude_fields", self.default_exclude_fields)

        super().__init__(*args, **kwargs)

        if fields:
            for field_name in set(self.fields) - set(fields):
                self.fields.pop(field_name)
        elif exclude_fields:
            for field_name in set(exclude_fields):
                self.fields.pop(field_name)


class OrderedModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer to provide a serializer that can be update and create
    objects in a specific order.
    """

    def check_count(self):
        ModelClass = self.Meta.model
        max_count = ModelClass.MAX_COUNT
        if (
            max_count is not None
            and max_count <= self.context["view"].get_queryset().count()
        ):
            raise serializers.ValidationError(
                "{model} max count reached. Ordered queryset cannot contain more than {value}.".format(
                    model=ModelClass.__name__,
                    value=max_count,
                )
            )

    def create(self, validated_data):
        self.check_count()
        return self._create_or_update(validated_data)

    def update(self, instance, validated_data):
        return self._create_or_update(validated_data, instance)

    def _create_or_update(self, validated_data, instance=None):
        """Create or update an instance."""
        order = validated_data.pop("order", None)

        if instance is None:
            instance = super().create(validated_data)
        else:
            instance = super().update(instance, validated_data)

        if isinstance(order, int):
            instance.to(order)
        return instance

    # def validate_order(self, value):
    #     if self.instance is not None and value not in list(
    #         self.get_queryset().values_list("order", flat=True)
    #     ):
    #         raise serializers.ValidationError(
    #             "Invalid order value. Expected value must be greater than or equal to 0 and less than the size of the related queryset."
    #         )
    #     return value


#


class UserModelSerializer(
    CamelModelSerializer,
    DynamicFieldsSerializer,
):
    """A Model Serializer for model instances from the `api__users` application."""

    pass


class OrderedUserModelSerializer(
    CamelModelSerializer,
    DynamicFieldsSerializer,
    OrderedModelSerializer,
):
    """An Ordered Model Serializer for model instances from the `api__users` application."""

    pass
