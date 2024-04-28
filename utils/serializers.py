from rest_framework import serializers


class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.\n
    Modified from DRF's example:
    https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude_fields = kwargs.pop("exclude_fields", None)

        super().__init__(*args, **kwargs)

        if fields == "__all__":
            pass
        elif fields:
            exclude = set(self.fields) - set(fields)
            for field_name in exclude:
                self.fields.pop(field_name)
        elif exclude_fields:
            for field_name in set(exclude_fields):
                self.fields.pop(field_name)


class OrderedModelSerializer(DynamicFieldsSerializer):
    """
    A ModelSerializer to provide a serializer that can be update and create
    objects in a specific order.
    """

    def validate_order(self, value):
        if self.instance is not None and value not in self.context["order_values"]:
            raise serializers.ValidationError(
                "Invalid order value. Expected value must be greater than or equal to 0 and less than the size of the related queryset."
            )
        return value

    def check_count(self):
        model_cls = self.Meta.model
        max_count = getattr(model_cls, "MAX_COUNT", None)
        if max_count is not None and self.context.get("qs_count") >= max_count:
            raise serializers.ValidationError(
                "{model} max count reached. Ordered queryset cannot contain more than {value}.".format(
                    model=model_cls.__name__,
                    value=max_count,
                )
            )

    def create(self, validated_data):
        self.check_count()
        return self._create_or_update(validated_data)

    def update(self, instance, validated_data):
        return self._create_or_update(validated_data, instance)

    def _create_or_update(self, validated_data, instance=None):
        """Create / Update an instance."""
        # order = None if "order" not in validated_data else validated_data.pop("order")
        order = validated_data.pop("order", None)

        if instance is None:
            instance = super().create(validated_data)
        else:
            instance = super().update(instance, validated_data)

        if isinstance(order, int):
            instance.to(order)
        return instance

    def get_max_count(self, obj):
        return self.Meta.model.MAX_COUNT
