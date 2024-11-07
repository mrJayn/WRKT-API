from datetime import date
from django.db import models
from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _
from utils.models import OrderedModel
from .profile import Profile


class Program(OrderedModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="programs",
    )
    name = models.CharField(
        _("name"),
        max_length=50,
        default=_("New Program"),
        blank=True,
    )
    startdate = models.DateField(
        _("start date"),
        auto_now_add=False,
        blank=True,
        null=True,
        default=now,
    )
    duration = models.PositiveIntegerField(
        _("duration"),
        default=4,
        blank=True,
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
    )

    MAX_COUNT = 3

    def __str__(self):
        return _("{} Program({})").format(self.profile.user, self.order)

    @property
    def _user(self):
        return self.profile.user


class Week(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="weeks",
    )
    week_id = models.PositiveIntegerField(editable=False)

    MIN_COUNT = 4
    MAX_COUNT = 16

    def __str__(self):
        return _("{} Week({})").format(self.program.__str__(), self.week_id)

    @property
    def _user(self):
        return self.profile.user
