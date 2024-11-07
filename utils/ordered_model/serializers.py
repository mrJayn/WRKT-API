from rest_framework import serializers


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

    def create(self, validated_data):
        self.check_count()
        return self._create_or_update(validated_data)

    def update(self, instance, validated_data):
        return self._create_or_update(validated_data, instance)

    """
    def validate_order(self, value):
        if self.instance is not None and value not in list(
            self.get_queryset().values_list("order", flat=True)
        ):
            raise serializers.ValidationError(
                "Invalid order value. Expected value must be greater than or equal to 0 and less than the size of the related queryset."
            )
        return value
    """
