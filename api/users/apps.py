from django.apps import AppConfig, apps
from django.db.models.signals import pre_save, post_save, post_delete


class UsersConfig(AppConfig):
    name = "api.users"
    label = "api_users"
    verbose_name = "users"

    def ready(self):
        pass
        # Implicitly connect signal handlers decorated with @receiver.
        # from . import signals

        # from .models import CustomUser, Profile

        # post_save.connect(Profile.create_user_profile, sender=CustomUser)
