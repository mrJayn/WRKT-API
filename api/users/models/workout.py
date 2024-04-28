from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import OrderedModel
from utils.managers import OrderedModelQuerySet
from utils.fields import ListField
from .profile import Profile


class WorkoutQuerySet(OrderedModelQuerySet):
    def update_active(self, ref):
        pk, is_active = getattr(ref, "pk"), getattr(ref, "is_active")
        if is_active != self.model.objects.get(pk=pk).is_active:
            qs = self.exclude(pk=pk)
            if is_active:
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


class WorkoutManager(models.Manager.from_queryset(WorkoutQuerySet)):
    pass


class Workout(OrderedModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="workouts",
        null=True,
    )
    name = models.CharField(
        _("name"),
        max_length=50,
        blank=True,
        default=_("New Workout"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
    )

    # day_names = ListField()

    MAX_COUNT = 3

    objects = WorkoutManager()

    def __str__(self):
        return _("{} Workout({})").format(self.profile.user, self.order)

    def save(self, *args, **kwargs):
        qs = self.get_ordered_queryset()
        if self.pk:
            qs.update_active(self)
        elif not qs.exists():  #  qs.filter(is_active=True).exists()
            self.is_active = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        is_active = self.is_active
        super().delete(*args, **kwargs)
        if is_active:
            self.get_ordered_queryset().activate_next()


# =======


class Day(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="days")
    day_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return _("{} Day({})").format(self.workout.__str__(), self.day_id)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = _("Day %s" % self.day_id)
        return super().save(*args, **kwargs)

    """
    bodyparts = ["chest", "back", "arms", "shoulders", "legs", "core"]
    """
