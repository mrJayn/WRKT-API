from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import Group

from api.utils.helpers import safeindex
from api.users.admin import USER_MODELS_ORDER


admin.site.site_header = "Wrkt administration."
admin.site.unregister(Group)


APP_ORDER = [
    "users",
    "exercise library",
]


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    # Sort the apps.
    app_list = sorted(
        app_dict.values(),
        key=lambda x: safeindex(x["name"].lower(), APP_ORDER),
    )
    # Sort the models within each app.
    for app in app_list:
        if app["name"] == "users":
            app["models"].sort(
                key=lambda x: safeindex(x["object_name"], USER_MODELS_ORDER)
            )
        else:
            app["models"].sort(key=lambda x: x["name"])
    return app_list


admin.AdminSite.get_app_list = get_app_list
