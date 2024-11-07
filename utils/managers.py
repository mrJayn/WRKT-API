from django.db import models
from django.db.models import F, Max
from django.utils.translation import gettext_lazy as _


class OrderedModelQuerySet(models.QuerySet):

    def get_next_order(self):
        """Get the next order value for the queryset."""
        max_order = self.aggregate(Max("order")).get("order__max")
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
        return self.update(**{"order": F("order") + value})


class OrderedModelManager(models.Manager.from_queryset(OrderedModelQuerySet)):
    pass


# ========== ========== ==========


class _UniqueActiveOrderedModelQuerySet(models.QuerySet):
    def update_active(self, ref):
        """
        Update the "active" instance status changes,
        """
        if not ref.pk:
            return

        wrt_map = {
            f.name: getattr(ref, f.name)
            for f in ref._meta.concrete_fields
            if isinstance(f, models.ForeignKey)
        }

        qs = self.filter(**wrt_map)
        if ref.is_active != qs.get(pk=ref.pk).is_active:
            qs = qs.exclude(pk=ref.pk)
            if ref.is_active:
                return qs.deactivate_all()
            return qs.activate_next()

    def deactivate_all(self):
        if self.exists() and self.filter(is_active=True).exists():
            return self.update(is_active=False)

    def activate_next(self):
        if self.exists():
            pk = self.first().pk
            self.filter(pk=pk).update(is_active=True)
            return self.exclude(pk=pk).deactivate_all()
