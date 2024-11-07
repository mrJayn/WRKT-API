from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.auth"
    label = "api_auth"
    verbose_name = _("API Authentication and Authorization")

    def ready(self):
        pass
