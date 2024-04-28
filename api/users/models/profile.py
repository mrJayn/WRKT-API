from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .custom_user import CustomUser


class Profile(models.Model):
    class Units(models.TextChoices):
        LBS = "LBS", "lbs"
        KGS = "KGS", "kgs"

    # class Presets(models.TextChoices):
    #     PPL = "PPL", "push, pull, legs"
    #     BDY = "BDY", "bodypart"
    #     BRO = "BRO", "bro"
    #     UPL = "UPL", "upper lower"

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )

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

    def __str__(self):
        return f"{self.user.username} Profile"

    # @property
    # def current_weekday(self):
    #     hrs = int(self.time_offset)
    #     mins = 60 * (hrs % 1)
    #     t = datetime.now() + timedelta(hours=hrs, minutes=mins)
    #     return date.weekday(t)
