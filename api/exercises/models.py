from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseExercise(models.Model):
    class Bodypart:
        NONE = ""
        CHST = "CHEST"
        BACK = "BACK"
        ARMS = "ARMS"
        SHLD = "SHOULDERS"
        LEGS = "LEGS"
        CORE = "CORE"

    class Equipment:
        NONE = ""
        BARB = "BARBELL"
        DUMB = "DUMBELL"
        SMTH = "SMITH_MACHINE"
        MACH = "MACHINE"
        CABL = "CABLE"
        EZBR = "EZ_BAR"
        BWGT = "BODY_WEIGHT"
        FWGT = "FREE_WEIGHT"
        BAND = "BANDED"

    BODYPART_CHOICES = (
        (Bodypart.CHST, _("Chest")),
        (Bodypart.BACK, _("Back")),
        (Bodypart.ARMS, _("Arms")),
        (Bodypart.SHLD, _("Shoulders")),
        (Bodypart.LEGS, _("Legs")),
        (Bodypart.CORE, _("Core")),
        (Bodypart.NONE, _("none")),
    )

    EQUIPMENT_CHOICES = (
        (Equipment.BARB, _("Barbell")),
        (Equipment.DUMB, _("Dumbell")),
        (Equipment.SMTH, _("Smith Machine")),
        (Equipment.MACH, _("Machine")),
        (Equipment.CABL, _("Cable")),
        (Equipment.EZBR, _("Ez Bar")),
        (Equipment.BWGT, _("Body-Weight")),
        (Equipment.FWGT, _("Free-Weight")),
        (Equipment.BAND, _("Banded")),
        (Equipment.NONE, _("none")),
    )

    name = models.CharField(_("name"), max_length=75)
    bodypart = models.CharField(
        _("bodypart"),
        max_length=9,
        choices=BODYPART_CHOICES,
        default=Bodypart.NONE,
    )
    equipment = models.CharField(
        _("equipment"),
        max_length=13,
        choices=EQUIPMENT_CHOICES,
        default=Equipment.NONE,
    )

    class Meta:
        permissions = [
            (
                "can_edit_defs",
                "Can change the name, bodypart, and equipment for the exercise",
            ),
        ]

    def __str__(self):
        return self.name


'''

class Exercise(BaseExercise):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("name"), max_length=75)
    bodypart = models.CharField(
        max_length=9,
        choices=ExerciseConstants.BODYPART_CHOICES,
        default="",
    )
    equipment = models.CharField(
        max_length=13,
        choices=ExerciseConstants.EQUIPMENT_CHOICES,
        default="",
    )
    orm = models.PositiveIntegerField(_("One Rep Max"), null=True, blank=True)
    is_enabled = models.BooleanField(_("Enabled"), default=True)
    is_custom = models.BooleanField(_("Custom"), default=True, editable=False)


# ========== ========== ==========


EXERCISE_TAG_CHOICES = (
    ("D", "Day"),
    ("W", "Week"),
)

class Exercise(OrderedModel):
    editor_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    editor_object_id = models.PositiveIntegerField()
    editor = fields.GenericForeignKey("editor_content_type", "editor_object_id")

    item_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    item_object_id = models.PositiveIntegerField()
    item = fields.GenericForeignKey("detail_content_type", "detail_object_id")
    #
    # editor = models.ForeignKey(__CLASS__, on_delete=models.CASCADE,related_name="exercises")
    ref = models.ForeignKey(RefExercise, blank=True, null=True)
    name = models.CharField(_("name"), max_length=75)

    def __str__(self):
        return "%s %s" % (self.editor.name, self.name)

    @property
    def user(self):
        return self.editor.group.user

    @classmethod
    def _on_exercise_save(cls, sender=None, instance=None, created=False, **kwargs):
        if created or did_field_change(instance, "name"):
            ref_obj = RefExercise.objects.get(
                user=instance.user,
                name=instance.name,
            )
            if ref_obj != instance.ref:
                setattr(instance, "ref", ref_obj)


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
        return _("%s Set%d") % (self.exercise.name, self.order)

    @property
    def user(self):
        return self.exercise.user

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
