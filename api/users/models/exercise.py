from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import OrderedModel

from .workout import Day
from .program import Week
from .library import LibraryExercise


def get_library_reference(name: str):
    try:
        return LibraryExercise.objects.get(name=name.lower().replace(" ", "_"))
    except ObjectDoesNotExist:
        return None


class ExerciseSetModelBase(models.Model):
    sets = models.CharField(max_length=50, default="", blank=True)
    reps = models.CharField(max_length=50, default="", blank=True)
    weight = models.CharField(max_length=50, default="", blank=True)
    percent = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_library_ref(self):
        return self.exercise.library_ref

    @property
    def units(self):
        return self.exercise.units

    @property
    def calculated_weight(self):
        library_ref = self.get_library_ref()
        if not self.percent or not library_ref or not library_ref.max:
            return None
        units = self.exercise.units
        base = 5 if units == "lbs" else 1.25
        raw_weight = self.percent * int(library_ref.max)
        if units != "kgs":
            raw_weight *= 0.45359237
        return round(base * round(float(raw_weight) / base), 1)


class Exercise(OrderedModel):
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        related_name="exercises",
        blank=True,
        null=True,
    )
    week = models.ForeignKey(
        Week,
        on_delete=models.CASCADE,
        related_name="exercises",
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=50,
        default="",
        blank=True,
    )

    class Meta:
        ordering = ["day", "week", "order"]

    def __str__(self):
        return _("{} Exercise({})").format(
            (self.day or self.week).__str__(),
            self.order,
        )

    def get_max_count(self):
        day_limit, week_limit = 10, 3
        return day_limit if self.day is not None else week_limit

    @property
    def profile(self):
        if self.day is not None:
            return self.day.workout.profile
        elif self.week is not None:
            return self.week.program.profile

    @property
    def library_ref(self):
        return get_library_reference(self.name)

    @property
    def units(self):
        return "kgs" if self.profile.prefers_metric else "lbs"

    @property
    def _user(self):
        if self.day is not None:
            return self.day.workout.profile.user
        return self.week.program.profile.user


class ExerciseSet(ExerciseSetModelBase, OrderedModel):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="sets",
    )

    MAX_COUNT = 3

    def __str__(self):
        return _("{} Set({})").format(self.exercise.__str__(), self.order)

    @property
    def _user(self):
        return self.exercise._user


class SecondaryExercise(ExerciseSetModelBase):
    exercise = models.OneToOneField(
        Exercise,
        on_delete=models.CASCADE,
        related_name="secondary",
    )
    name = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return _("{} Secondary").format(self.exercise.__str__())

    def get_library_ref(self):
        return self.library_ref

    @property
    def library_ref(self):
        return get_library_reference(self.name)

    @property
    def _user(self):
        return self.exercise._user
