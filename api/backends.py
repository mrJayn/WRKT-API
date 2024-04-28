from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UsernameFieldAuthentication(BaseBackend):
    """
    An authentication plugin that authenticates a set of user credentials
    provided in the request body, which contains either an email address
    or phone-number, and a password.
    """

    def authenticate(self, request, email_or_phone=None, password=None):
        """
        Returns a `User` if the supplied credentials are valid,
        otherwise returns `None`.
        """
        try:
            user = User.objects.get(
                Q(email=email_or_phone) | Q(phone_number=email_or_phone)
            )
        except User.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
