from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model


def did_field_change(cls, field_name):
    if not issubclass(type(cls), Model):
        raise TypeError("did_field_change() `ref` must be a Model subclass.")

    if not cls or not cls.pk:
        return False

    try:
        cls._meta.get_field(field_name)
    except FieldDoesNotExist:
        raise ValueError(
            "%s is not a field for the %s model." % (field_name, cls._meta.model_name)
        )

    obj = cls._meta.default_manager.get(pk=cls.pk)
    return getattr(cls, field_name) != getattr(obj, field_name)


def safeindex(key, sort_list):
    if key not in sort_list:
        return ord(key[0])
    return sort_list.index(key)
