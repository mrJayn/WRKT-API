from typing import Any
from django.core import checks
from django.db import models
from django.utils.translation import gettext_lazy as _

import utils
from utils.managers import OrderedModelManager


"""
Modified from: https://github.com/django-ordered-model/django-ordered-model/blob/master/ordered_model/models.py
"""


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
        filter_kwargs = self._wrt_map(ref=self)
        return self._meta.default_manager.all().filter(**filter_kwargs)

    def get_max_count(self):
        return self.MAX_COUNT

    @classmethod
    def _wrt_map(cls, ref):
        fields = cls._meta.concrete_fields
        wrt_map = {}
        for field in fields:
            if isinstance(field, models.ForeignKey):
                field_name = field.name
                wrt_map[field_name] = getattr(ref, field_name)
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
    order = models.PositiveIntegerField(
        _("order"),
        db_index=True,
    )

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
