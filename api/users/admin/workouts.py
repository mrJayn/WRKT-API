from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from utils._admin.helpers import create_links_from_queryset

from api.users.models import Workout, Day
from .options import InlineModelAdmin


class InlineDayAdmin(InlineModelAdmin):
    model = Day
    fields = ["day_index", "name", "exercise_names"]
    readonly_fields = ["day_index", "exercise_names"]

    def has_change_permission(self, request, obj):
        return True

    @admin.display(description="Exercises")
    def exercise_names(self, obj):
        exercises_qs = None  # Exercise.objects.filter(day__pk=obj.pk)
        return create_links_from_queryset(exercises_qs, label_field="name")


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    actions = None
    inlines = (InlineDayAdmin,)
    fields = ("profile", "name")
    readonly_fields = ("profile",)
    list_display = ("_title", "_day_links")
    list_filter = ("profile",)
    ordering = ("profile", "order")

    @admin.display()
    def _title(self, obj):
        return "%s - %s" % (str(obj.profile.user), obj.name)

    @admin.display(description="Days")
    def _day_links(self, obj):
        days_qs = Day.objects.filter(workout__pk=obj.pk)
        return create_links_from_queryset(days_qs, label_field="name")


# ========== ========== ==========


# class InlineExerciseAdmin(admin.TabularInline):
#     model = Exercise
#     fields = ["day", "name", "order"]
#     readonly_fields = ["day"]
#     extra = 0


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    actions = None
    # inlines = (InlineExerciseAdmin,)
    fields = ("workout", "name")
    readonly_fields = ("workout",)
    list_display = ("_title",)
    list_filter = ("workout__profile",)
    ordering = ("workout", "day_index")

    def get_list_filter(self, request):
        if "workout__profile__id__exact" in request.GET:
            return self.list_filter + ("workout",)
        return self.list_filter

    @admin.display()
    def _title(self, obj):
        return "%s - %s - %s" % (
            str(obj.workout.profile.user),
            str(obj.workout),
            obj.name,
        )
