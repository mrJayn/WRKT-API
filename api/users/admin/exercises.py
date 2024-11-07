from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from api.users.models.exercise import CustomExercise


@admin.register(CustomExercise)
class CustomExerciseAdmin(admin.ModelAdmin):
    fields = ["user", "name", "bodypart", "equipment", "orm", "is_enabled"]
    readonly_fields = ["user"]

    def get_readonly_fields(self, request, obj):
        if obj and obj.pk:
            return self.readonly_fields
        return []


# ========== ========== ==========

"""

class ExerciseSetInline(admin.TabularInline):
    model = ExerciseSet
    max_num = ExerciseSet.MAX_COUNT
    extra = 0


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    inlines = (ExerciseSetInline,)
    model = Exercise
    fields = ["day", "week", "name", "order"]
    # list_filter = [ParentListFilter]


class ParentListFilter(admin.SimpleListFilter):
    title = _("parent")
    parameter_name = "day"

    def lookups(self, request, model_admin):
        return [("wkt", _("Workout")), ("prg", _("Program"))]

    def queryset(self, request, queryset):
        if self.value() == "wkt":
            return queryset.filter(program_week=None)
        if self.value() == "prg":
            return queryset.filter(workout_day=None)
"""
