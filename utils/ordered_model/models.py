"""
Modified `OrderedModel` from the "django-ordered-model" library.

Source:  
https://github.com/django-ordered-model/django-ordered-model/blob/master/ordered_model/models.py
"""

from django.core import checks
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderedModelQuerySet(models.QuerySet):

    def get_next_order(self):
        """Get the next order value for the queryset."""
        max_order = self.aggregate(models.Max("order")).get("order__max")
        return max_order + 1 if max_order is not None else 0

    def remove_ref(self, ref=None):
        """Decrease order values for objects located above the ref."""
        return self.filter(**{"order__gt": getattr(ref, "order")})._shift_orders(-1)

    def move_ref_to(self, ref, order):
        """Move the ref to the specified order and update all affected items."""
        og_order = getattr(ref, "order")
        if order == og_order:  # or not self._is_valid_order(order)
            return
        if og_order > order:
            lookup = {"order__lt": og_order, "order__gte": order}
            return self.filter(**lookup)._shift_orders(1)
        else:
            lookup = {"order__gt": og_order, "order__lte": order}
            return self.filter(**lookup)._shift_orders(-1)

    def _shift_orders(self, value):
        """Increase or decrease all objects order by a value."""
        return self.update(**{"order": models.F("order") + value})


class OrderedModelManager(models.Manager.from_queryset(OrderedModelQuerySet)):
    pass


class OrderedModelBase(models.Model):
    """
    An abstract model that allows objects to be ordered relative to their related parent.
    Provides an `order` field and the attributes `min_count` and `MAX_COUNT`,
    which constrain the number of models per ordered queryset.
    """

    MAX_COUNT = None

    objects = OrderedModelManager()

    class Meta:
        abstract = True

    def __str__(self):
        return _("{} {} {}").format(self._user, self.__class__.__name__, self.order)

    def get_ordered_queryset(self):
        filter_kwargs = self._wrt_map()
        return self._meta.default_manager.filter(**filter_kwargs)

    def get_max_count(self):
        return self.MAX_COUNT

    def _wrt_map(self, serialize=None):
        wrt_map = {}
        for field in self._meta.concrete_fields:
            if isinstance(field, models.ForeignKey):
                obj = getattr(self, field.name)
                if serialize and isinstance(obj, models.Model):
                    obj = obj.pk
                wrt_map[field.name] = obj
        return wrt_map

    @property
    def _user(self):
        return getattr(self, "user", "")

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        #   check `MAX_COUNT`.
        max_count = getattr(cls, "MAX_COUNT")
        if max_count is not None and not isinstance(max_count, int):
            errors.append(
                checks.Error(
                    "OrderedModel subclass 'MAX_COUNT' value invalid. Expected an integer or None.",
                    obj=str(cls.__qualname__),
                    id="ordered_model.E002",
                )
            )
        #   check `get_max_count`.
        return errors


class OrderedModel(OrderedModelBase):
    order = models.PositiveIntegerField(_("order"), db_index=True)

    class Meta:
        abstract = True
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not isinstance(self.order, int):
            self.order = self.get_ordered_queryset().get_next_order()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.get_ordered_queryset().remove_ref(self)
        super().delete(*args, **kwargs)

    def to(self, order):
        self.get_ordered_queryset().move_ref_to(self, order)
        self.order = order
        self.save()


"""
    @classmethod
    def _wrt_map(cls,ref):
        fields = cls._meta.concrete_fields
        wrt_map={}
        for field in fields:
            if isinstance(field, models.ForeignKey):
                print(f"field >> {field}")
                wrt_map[field.name] = getattr(ref, field)
        return wrt_map
"""
