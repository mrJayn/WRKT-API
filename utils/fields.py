import json
from typing import Iterable
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UniqueCharField(models.CharField):
    """
    A `CharField` with option `unique` set to True and if `blank` is set
    to True, then `null` will also be set True.

    ( Follows the `CharField` exception that if options `unique`
    and `blank` are both True, then `null` is required to be True. )
    """

    description = _("Unique string")

    default_error_messages = {
        "unique": _("That %(field_label)s already exists."),
    }

    def __init__(self, blank=True, *args, **kwargs):
        if blank:
            kwargs["blank"] = True
            kwargs["null"] = True
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["null"]
        del kwargs["unique"]
        return name, path, args, kwargs


class OptionalUniqueCharField(UniqueCharField):
    #########   DELETE THIS    #########
    pass


class RangeIntegerField(models.IntegerField):
    """
    A `IntegerField` that provides a `MinValueValidator` and
    `MaxValueValidator` that can be set via the `range` option.
    ```
    # Validates min value of 0 and max value of 10
    field = RangeIntegerField( ... , range=[0, 10] , ... )
    ```
    """

    error_messages = {
        "invalid_range": _(
            "The value of `range` must be a list or tuple "
            "containing 2 or less integers."
        )
    }

    def __init__(self, range=None, *args, **kwargs):
        if range and isinstance(range, list):
            validators = kwargs.pop("validators", [])
            list_size = len(range)
            if list_size > 2:
                raise ValueError(self.error_messages["invalid_range"])
            validators.append(MinValueValidator(0 if len(range) < 2 else range[0]))
            validators.append(MaxValueValidator(range.pop()))
            kwargs["validators"] = validators
        super().__init__(*args, **kwargs)


class ListField(models.TextField):
    """
    A custom Django field to represent lists as comma separated strings
    https://stackoverflow.com/a/53384689
    """

    description = _("Text List")

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ",")
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["token"] = self.token
        return name, path, args, kwargs

    def to_python(self, value):

        class SubList(list):
            def __init__(self, token, *args):
                self.token = token
                super().__init__(*args)

            def __str__(self):
                return self.token.join(self)

        if isinstance(value, list):
            return value
        if value is None:
            return SubList(self.token)
        return SubList(self.token, value.split(self.token))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if not value:
            return
        assert isinstance(value, Iterable)
        return self.token.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
