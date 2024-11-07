from django.utils.translation import gettext_lazy as _


class Messages:
    INVALID_CREDENTIALS_ERROR = _("Unable to log in with provided credentials.")
    INACTIVE_ACCOUNT_ERROR = _(
        "User account is disabled."
    )  # not in use since Django 1.10
    INVALID_TOKEN_ERROR = _("Invalid token for given user.")
    INVALID_UID_ERROR = _("Invalid user id or user doesn't exist.")
    STALE_TOKEN_ERROR = _("Stale token for given user.")
    PASSWORD_MISMATCH_ERROR = _("The two password fields didn't match.")
    USERNAME_MISMATCH_ERROR = _("The two {0} fields didn't match.")
    INVALID_PASSWORD_ERROR = _("Invalid password.")
    EMAIL_NOT_FOUND = _("User with given email does not exist.")
    CANNOT_CREATE_USER_ERROR = _("Unable to create account.")


class Themes:
    LIGHT = _("Light")
    DARK = _("Dark")
    SYSTEM = _("System")


class WeightUnits:
    LBS = _("lbs")
    KGS = _("kgs")


class Bodyparts:
    CHST = _("Chest")
    BACK = _("Back")
    ARMS = _("Arms")
    SHLD = _("Shoulders")
    LEGS = _("Legs")
    ABS = _("Core")


class Equipments:
    BB = _("Barbell")
    DB = _("Dumbell")
    SM = _("Smith Machine")
    MACH = _("Machine")
    CABL = _("Cable")
    EZ = _("Ez Bar")
    BODY = _("Body-Weight")
    FREE = _("Free-Weight")
    BAND = _("Banded")
