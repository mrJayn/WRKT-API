from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from utils.country_codes import CountryCodes

UserModel = settings.AUTH_USER_MODEL


class Profile(models.Model):
    class Units(models.TextChoices):
        LBS = "lbs", "lbs"
        KGS = "kgs", "kgs"

    class Theme(models.TextChoices):
        LIGHT = "light", "Light"
        DARK = "dark", "Dark"
        SYSTEM = "system", "System"

    # class Presets(models.TextChoices):
    #     PPL = "PPL", "push, pull, legs"
    #     BDY = "BDY", "bodypart"
    #     BRO = "BRO", "bro"
    #     UPL = "UPL", "upper lower"

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    notifications = models.BooleanField(default=False)
    day_one_wkday = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(6)],
    )
    units = models.CharField(
        default=Units.LBS,
        choices=Units.choices,
        max_length=3,
    )
    theme = models.CharField(
        default=Theme.SYSTEM,
        choices=Theme.choices,
        max_length=6,
    )
    locale = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        choices=CountryCodes.choices,
        default=CountryCodes.US,
    )

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return "%s Profile" % self.user

    # @property
    # def current_weekday(self):
    #     hrs = int(self.time_offset)
    #     mins = 60 * (hrs % 1)
    #     t = datetime.now() + timedelta(hours=hrs, minutes=mins)
    #     return date.weekday(t)


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
