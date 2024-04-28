from phonenumber_field import phonenumber
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField
from django.conf import settings
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_email_or_phone_number(value):
    try:
        validate_email(value)
    except ValidationError(_("Invalid email.")):
        phone_number = phonenumber.to_python(value)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(_("Invalid email or phone number."))


class EmailOrPhoneNumberField(CharField):
    default_error_messages = {
        "invalid": _("Enter a valid email address or mobile phone number.")
    }

    def __init__(self, *args, region=None, **kwargs):
        kwargs["max_length"] = 256

        super().__init__(*args, **kwargs)

        phonenumber.validate_region(region)
        self.region = region or getattr(settings, "PHONENUMBER_DEFAULT_REGION", None)
        self.validators.append(validate_email_or_phone_number)
