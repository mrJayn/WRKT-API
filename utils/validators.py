from phonenumber_field import phonenumber
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_email
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

"""
source: https://stackoverflow.com/questions/3868753/find-usa-phone-numbers-in-python-script
"""


@deconstructible
class PhoneNumberValidator(RegexValidator):
    regex = r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$"
    message = _("Enter a valid phone number.")
    flags = 0


phone_number_re = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
validate_phone_number = RegexValidator(
    phone_number_re,
    _("Enter a valid phone number."),
    "invalid",
)


def is_email(value):
    try:
        validate_email(value)
    except ValidationError:
        return False
    return True


def is_phonenumber(value):
    phone_number = phonenumber.to_python(value)
    return phone_number and phone_number.is_valid()
