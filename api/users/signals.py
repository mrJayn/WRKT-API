from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from api.users.models import Workout, Day, Program, Week

# New user has registered.
user_registered = Signal()

# User activated their account.
user_activated = Signal()

# User has been updated.
user_updated = Signal()


# New Workout created.
@receiver(post_save, sender=Workout)
def add_days(sender, instance, created, **kwargs):
    """
    Create `Day` models related to the workout instance if it was created.
    """
    if created:
        for n in range(getattr(instance, "num_days", Day.MIN_COUNT)):
            Day.objects.get_or_create(
                workout=instance,
                day_index=(n + 1),
                name="Day %d" % (n + 1),
            )


# New Program created
@receiver(post_save, sender=Program)
def add_weeks(sender, instance, created, **kwargs):
    """
    Create `Week` models related to the program instance if it was created.
    """
    if created:
        for n in range(getattr(instance, "duration", Week.MIN_COUNT)):
            Week.objects.get_or_create(
                program=instance,
                week_id=(n + 1),
            )
