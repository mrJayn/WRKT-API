from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

from . import default_settings


USER_SETTINGS_NAMESPACE = "USER_SETTINGS"

SETTINGS_TO_IMPORT = (
    "SERIALIZERS",
    "EMAIL",
    "CONSTANTS",
    "PERMISSIONS",
    "TOKEN_MODEL",
    "SOCIAL_AUTH_TOKEN_STRATEGY",
    "WEBAUTHN",
)


class ImportDict(dict):
    def __getattribute__(self, item):
        try:
            val = self[item]
            if isinstance(val, str):
                val = import_string(val)
            elif isinstance(val, (list, tuple)):
                val = [import_string(v) if isinstance(v, str) else v for v in val]
            self[item] = val
        except KeyError:
            val = super().__getattribute__(item)

        return val


class Settings:
    def __init__(self):
        # Load default settings.( but only for ALL_CAPS settings )
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        explicit_settings = getattr(django_settings, USER_SETTINGS_NAMESPACE, {})

        # Override from values of `USER_SETTINGS_NAMESPACE` in django_settings.
        for setting, setting_value in explicit_settings.items():
            value = setting_value
            if isinstance(setting_value, dict):
                value = getattr(self, setting, {})
                value.update(setting_value)
                value = ImportDict(value)
            setattr(self, setting, value)

        # Import dotted path string settings
        for setting in SETTINGS_TO_IMPORT:
            value = getattr(self, setting)
            setattr(self, setting, import_string(value))

    def __import_value(self, setting):
        val = getattr(self, setting)
        if isinstance(val, str):
            val = import_string(val)
        elif isinstance(val, (list, tuple)):
            val = [import_string(v) if isinstance(v, str) else v for v in val]
        elif isinstance(val, dict):
            val = {k: self.import_value(v) for k, v in val.items()}
        return val


class LazySettings(LazyObject):
    def _setup(self):
        self._wrapped = Settings()


settings = LazySettings()


def reload_user_settings(*args, **kwargs):
    global settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == USER_SETTINGS_NAMESPACE:
        settings._setup(explicit_overriden_settings=value)


setting_changed.connect(reload_user_settings)
