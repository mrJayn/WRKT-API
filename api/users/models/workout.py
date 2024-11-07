from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.db.models import UniqueConstraint, signals
from django.db.models.functions import Lower
from django.db.models.sql.query import Query
from django.utils.translation import gettext_lazy as _

from utils.models import OrderedModel
from utils.managers import OrderedModelQuerySet

from api.utils.helpers import did_field_change
from .profile import Profile


class WorkoutQuerySet(OrderedModelQuerySet):
    def update_active(self, instance):
        qs = instance.get_ordered_queryset()

        # Created instance is the only ordered object, so it must be active.
        if not qs.exists() and not instance.is_active:
            setattr(instance, "is_active", True)

        # If `is_active` has changed, then update the other ordered objects accordingly.
        elif did_field_change(instance, "is_active"):
            qs = qs.exclude(pk=instance.pk)
            if not qs.exists():
                return

            # If ref was deactivated, then activate the next available instance.
            if not instance.is_active:
                next_pk = qs.first().pk
                qs.filter(pk=next_pk).update(is_active=True)
                qs = qs.exclude(pk=next_pk)

            # Deactivate other active instances.
            qs.filter(is_active=True).update(is_active=False)

    def activate_next(self):
        if self.exists():
            self.filter(pk=self.first().pk).update(is_active=True)

    def deactivate_all(self):
        return self.update(is_active=False)

    def _check_active(self, ref):
        qs = ref.get_ordered_queryset()
        if qs.exists() and qs.filter(is_active=True).count() != 1:
            fallback_pk = ref.pk if ref.is_active else qs.first().pk
            qs.filter(pk=fallback_pk).update(is_active=True)
            qs.exclude(pk=fallback_pk).update(is_active=False)


class Workout(OrderedModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="workouts",
    )
    name = models.CharField(
        _("name"),
        max_length=50,
        blank=True,
        default=_("New Workout"),
    )
    is_active = models.BooleanField(_("active"), default=False)

    MIN_COUNT = 0
    MAX_COUNT = 3

    objects = WorkoutQuerySet.as_manager()

    """
    class Meta:
        constraints = [
            UniqueConstraint(Lower("name").desc(), "profile", name="unique_lower_name_profile"),
        ]
    """

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.objects.update_active(self)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ref = self
        super().delete(*args, **kwargs)
        if ref.is_active:
            ref.get_ordered_queryset().activate_next()


# ========== ========== ==========


class Day(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="days",
    )
    name = models.CharField(
        max_length=50,
        default="",
    )
    day_index = models.PositiveIntegerField(default=0)

    # gen_exercises = fields.GenericRelation("GenericExercise")

    MIN_COUNT = 7
    MAX_COUNT = 7

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "Day %d" % self.day_index
        return super().save(*args, **kwargs)


# ========== ========== ==========
