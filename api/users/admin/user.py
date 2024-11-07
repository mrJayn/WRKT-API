from typing import Any
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from utils._admin.helpers import model_reverse
from api.users.models import CustomUser, Profile, Workout, Program


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Change Form
    fieldsets = (
        (_("Account"), {"fields": ("username", "email", "phone_number", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_superuser", "user_permissions", "groups")},
        ),
        (_("Dates"), {"fields": ("date_joined", "last_login")}),
        (_("Active Status"), {"fields": ("is_active",)}),
    )
    readonly_fields = ("last_login", "date_joined")

    # Add Form
    add_fieldsets = (
        (
            None,
            {"fields": ("email", "phone_number", "password1", "password2")},
        ),
    )
    # Change Password Form

    # Change List Form
    list_display = ("__str__", "email", "phone_number", "is_active", "is_superuser")
    list_filter = ("is_active", "is_superuser")
    search_fields = ("email", "phone_number", "username")
    ordering = ("-is_active", "id")

    def get_fieldsets(self, request, obj=None):
        """Add "wide" style to each fieldset."""
        fieldsets = super().get_fieldsets(request, obj)
        for _, fieldset in fieldsets:
            fieldset.setdefault("classes", ("wide",))
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # If the user is inactive, then add the inactive timeout string to the help text.
        if obj and not obj.is_active:
            extra_help_text = (
                '<br/>⚠️<span style="color: #ffbd57;"> Delete in: [ %s ]</span>'
                % obj.get_inactive_timeout_str()
            )
            form.base_fields["is_active"].help_text += extra_help_text

        # If the user is not a superuser, remove edit permissions.
        if not request.user.is_superuser:
            form.base_fields["is_superuser"].disabled = True

        return form

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["customuser_links"] = self.get_rel_links(object_id)
        return super().change_view(request, object_id, form_url, extra_context)

    def get_rel_links(self, object_id):
        profile = Profile.objects.get(user__id=object_id)
        model_links = [
            (Profile, {"args": [profile.id]}),
            (Workout, {"query": {"profile": profile.id}}),
            (Program, {"query": {"profile": profile.id}}),
        ]
        return [
            {
                "name": model._meta.verbose_name_plural,
                "href": model_reverse(model, **kwargs),
            }
            for model, kwargs in model_links
        ]
