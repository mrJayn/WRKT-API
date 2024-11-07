import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.users.models.profile import Profile


EXERCISE_PRESETS_URL = "static/exercise_data.json"


class LibraryManager(models.Manager):
    def create(self, name, **extra_fields):
        extra_fields.setdefault("is_custom", True)
        return super().create(name, **extra_fields)

    def create_preset(self, **extra_fields):
        extra_fields.setdefault("is_custom", False)
        if extra_fields.get("is_custom") is not True:
            raise ValueError("Preset Library Exercises must have is_custom set False.")
        return self.create(**extra_fields)

    # def bulk_create_presets(self, raw_objs):
    #     objs = [self.model(**obj) for obj in raw_objs]
    #     return self.bulk_create(objs)


class LibraryExercise(models.Model):
    NONE = ""
    CHST = "CHEST"
    BACK = "BACK"
    ARMS = "ARMS"
    SHLD = "SHOULDERS"
    LEGS = "LEGS"
    CORE = "CORE"
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
        (CHST, _("Chest")),
        (BACK, _("Back")),
        (ARMS, _("Arms")),
        (SHLD, _("Shoulders")),
        (LEGS, _("Legs")),
        (CORE, _("Core")),
        (NONE, _("none")),
    )

    EQUIPMENT_CHOICES = (
        (BARB, _("Barbell")),
        (DUMB, _("Dumbell")),
        (SMTH, _("Smith Machine")),
        (MACH, _("Machine")),
        (CABL, _("Cable")),
        (EZBR, _("Ez Bar")),
        (BWGT, _("Body-Weight")),
        (FWGT, _("Free-Weight")),
        (BAND, _("Banded")),
        (NONE, _("none")),
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="library",
    )
    name = models.CharField(max_length=100)
    bodypart = models.CharField(max_length=9, choices=BODYPART_CHOICES, default=NONE)
    equipment = models.CharField(max_length=13, choices=EQUIPMENT_CHOICES, default=NONE)
    enabled = models.BooleanField(default=True)
    max = models.PositiveIntegerField(null=True, blank=True)
    is_custom = models.BooleanField(default=True, editable=False)

    objects = LibraryManager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

    @classmethod
    def create_default_library(cls, profile):
        if cls.objects.filter(profile=profile).exists():
            return

        with open(EXERCISE_PRESETS_URL) as f:
            dct = json.load(f)

        # exercise_objs = [{"profile": profile, **{k: str(v) for k, v in obj.items()}}for obj in dct["data"]]

        for obj in dct["data"]:
            extra_fields = {k: str(v) for k, v in obj.items()}
            cls.objects.create_preset(profile=profile, **extra_fields)
