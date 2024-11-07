from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.core import checks, mail, exceptions
from django.db import models
from django.utils.text import capfirst
from django.utils.timezone import timedelta, now
from django.utils.timesince import timesince, timeuntil

from django.utils.translation import gettext_lazy as _

from utils.time import strftimedelta

from api.utils.helpers import did_field_change


"""
Django `AbstractUser`:  https://docs.djangoproject.com/en/5.0/ref/contrib/auth/

"ISO-3166-1" is the two letter country code, used to interpret phone numbers.
"""


class CustomUserManager(UserManager):

    def _create_user(self, email, phone_number, password, **extra_fields):
        """
        Create and save a user with the given either `email`
        or `phone_number` (or both) and `password`.
        """
        if not email and not phone_number:
            raise ValueError("Either the given email or phone-number must be set")
        if email:
            email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, phone_number, password, **extra_fields)

    def create_superuser(self, email, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    A custom auth user model.

    Both `email` or `phone-number` can be used as a uuid, and at least one is required.
    """

    username_validator = UnicodeUsernameValidator()

    _is_active = True

    email = models.EmailField(
        _("email address"),
        unique=True,
        blank=True,
        null=True,
        error_messages={"unique": _("This email address is already being used.")},
    )

    phone_number = PhoneNumberField(
        _("phone number"),
        unique=True,
        blank=True,
        null=True,
        error_messages={"unique": _("This phone number is already being used.")},
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        default="",
        validators=[username_validator],
    )

    inactive_start_date = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        constraints = [
            models.CheckConstraint(
                name="email_or_phone_number",
                check=(
                    (~models.Q(email="") & models.Q(email__isnull=False))
                    | (
                        ~models.Q(phone_number="")
                        & models.Q(phone_number__isnull=False)
                    )
                ),
            )
        ]

    def __str__(self):
        # "User{}".format(self.pk)
        return self.username or capfirst(self.email.split("@", 1)[0])

    def save(self, *args, **kwargs):
        # Update the inactive start datetime if activity status changes.
        if did_field_change(self, "is_active"):
            self.inactive_start_date = None if self.is_active else now()
        super().save(*args, **kwargs)

    def email_user(self, subject, message, from_email=None, **kwargs):
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
        return super().email_user(subject, message, from_email, **kwargs)

    @property
    def timesince_last_login(self):
        return timesince(self.last_login)

    def get_inactive_timeout_str(self):
        """
        Return a timedelta to represent the amount of time until an inactive user will be terminated.
        If the user is active, then return None.
        """
        if self.is_active:
            return
        td = timedelta(days=settings.INACTIVE_USER_LIFESPAN_DAYS)
        if self.inactive_start_date is not None:
            del_dt = self.inactive_start_date + timedelta(
                days=settings.INACTIVE_USER_LIFESPAN_DAYS
            )
            td = del_dt - now()
        return strftimedelta(td)
