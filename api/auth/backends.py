from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


class _UserModelBackend(ModelBackend):
    def authenticate(self, request, email=None, phone_number=None, password=None):
        if (email is None and phone_number is None) or password is None:
            return
        try:
            user = UserModel.objects.get(Q(email=email) | Q(phone_number=phone_number))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
