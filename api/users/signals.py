from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from api.users.models import *


@receiver(post_save, sender=Workout)
def add_days(sender, instance, created, **kwargs):
    """A `Workout` post save signal which creates it's related `Day` models."""
    if created:
        for day_num in range(1, 8):
            Day.objects.get_or_create(
                workout=instance,
                day_id=day_num,
                name=_("Day %s" % day_num),
            )


@receiver(post_save, sender=Program)
def add_weeks(sender, instance, created, **kwargs):
    """A `Program` post save signal which creates it's related `Week` models."""
    if created:
        for week_id in range(1, (instance.duration + 1)):
            Week.objects.get_or_create(program=instance, week_id=week_id)
