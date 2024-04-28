import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from .profile import Profile

LIBRARY_PATH = "static/exercises_library/flat_data.json"


def name_serializer(s, to_repr=False):
    a, b = (" ", "_") if to_repr else ("_", " ")
    return str(s).replace(a, b)


class LibraryManager(models.Manager):
    def create(self, **kwargs):
        kwargs["custom"] = True
        return super().create(**kwargs)

    def create_default(self, **kwargs):
        kwargs.pop("custom", None)
        return super().create(custom=False, **kwargs)


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
        Profile, on_delete=models.CASCADE, related_name="library"
    )
    name = models.CharField(max_length=100)
    bodypart = models.CharField(max_length=9, choices=BODYPART_CHOICES, default=NONE)
    equipment = models.CharField(max_length=13, choices=EQUIPMENT_CHOICES, default=NONE)
    enabled = models.BooleanField(default=True)
    max = models.PositiveIntegerField(null=True, blank=True)
    custom = models.BooleanField(default=True, editable=False)

    objects = LibraryManager()

    class Meta:
        ordering = ["custom", "id"]

    def __str__(self):
        return "{_type} Library Exercise: {name}".format(
            _type="Custom" if self.custom else "Default",
            name=self.name,
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @classmethod
    def create_default_library(cls, profile):
        if cls.objects.filter(profile=profile).exists():
            return
        with open(LIBRARY_PATH, "r") as f:
            library = json.load(f)
        for ex in library.get("data"):
            # name, equipment, bodypart = ex.values()
            name, equipment, bodypart = [str(v) for v in ex.values()]
            cls.objects.create_default(
                profile=profile,
                name=name,
                equipment=equipment,
                bodypart=bodypart,
            )
