from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from api.users.models import Profile, Workout, Program
from .options import InlineModelAdmin


class InlineWorkoutAdmin(InlineModelAdmin):
    model = Workout


class InlineProgramAdmin(InlineModelAdmin):
    model = Program


# class InlineLibraryExerciseAdmin(InlineModelAdmin):
#     model = LibraryExercise
#     max_num = 20
#     filter_kwargs = {"is_custom": True}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    actions = None
    fieldsets = [
        (None, {"fields": ("user",)}),
        (
            _("Settings"),
            {"fields": ("notifications", "day_one_wkday", "units", "theme")},
        ),
    ]
    readonly_fields = ["user"]
    list_display = ["__str__", "user"]
    inlines = (
        InlineWorkoutAdmin,
        InlineProgramAdmin,
    )
