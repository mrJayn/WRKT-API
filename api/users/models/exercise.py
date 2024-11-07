from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import fields

from django.utils.translation import gettext_lazy as _

from utils.managers import OrderedModelQuerySet
from utils.models import OrderedModel

from .workout import Day
from .program import Week

from api.exercises.models import BaseExercise


class CustomExercise(BaseExercise):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orm = models.PositiveIntegerField(_("one rep max"), null=True, blank=True)
    is_enabled = models.BooleanField(_("enabled"), default=True)

    def __str__(self):
        return self.name


class Exercise(OrderedModel):
    pass
    """
    editor_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    editor_id = models.PositiveIntegerField()
    editor = GenericForeignKey("editor_type", "editor_id")
    """


# ========== ========== ==========


'''
# ========== ========== ==========
# ==========         OLD       ==========
# ========== ========== ==========


class Exercise(OrderedModel):
    
    # editor_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # editor_object_id = models.PositiveIntegerField()
    # editor = GenericForeignKey("editor_content_type", "editor_object_id")

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
        return _("{prefix} Exercise_{order}").format(
            prefix=(self.day or self.week).__str__(),
            order=self.order,
        )

    def get_max_count(self):
        day_limit, week_limit = 10, 3
        return day_limit if self.day is not None else week_limit

    def get_related_library_exercise_obj(self):
        filter_kwargs = {
            "profile": self.profile,
            "name": self.name.lower().replace(" ", "_").strip(),
        }
        try:
            return LibraryExercise.objects.get(**filter_kwargs)
        except LibraryExercise.DoesNotExist:
            return None

    @property
    def profile(self):
        if self.day is not None:
            return self.day.workout.profile
        elif self.week is not None:
            return self.week.program.profile

    @property
    def library_exercise(self):
        return self.get_related_library_exercise_obj()

    @property
    def _user(self):
        if self.day is not None:
            return self.day.workout.profile.user
        return self.week.program.profile.user


# ========== ========== ==========


class ExerciseSet(OrderedModel):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="sets",
    )
    sets = models.CharField(max_length=50, default="", blank=True)
    reps = models.CharField(max_length=50, default="", blank=True)
    weight = models.CharField(max_length=50, default="", blank=True)
    percent = models.FloatField(null=True, blank=True)

    MAX_COUNT = 3

    def __str__(self):
        return _("{} Set({})").format(self.exercise.__str__(), self.order)

    def get_library_ref(self):
        return self.exercise.library_exercise

    @property
    def _user(self):
        return self.exercise._user

    @property
    def units(self):
        return self.exercise.profile.units

    @property
    def calculated_weight(self):
        """
        **Required**
        Requires that the name related Library Exercise must exist, be related to an
        active `Program`, and have a percent defined for the current `Week`.
            -
        """
        if not self.percent:
            return None

        related_library_obj = self.exercise.library_exercise
        if not related_library_obj or not related_library_obj.max:
            return

        units = self.exercise.profile.units
        base = 5 if units == "lbs" else 1.25
        raw_weight = self.percent * int(related_library_obj.max)
        if units != "kgs":
            raw_weight *= 0.45359237
        return round(base * round(float(raw_weight) / base), 1)
'''
