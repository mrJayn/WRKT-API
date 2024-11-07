from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from utils._admin.helpers import create_links_from_queryset

from api.users.models import Program, Week
from .options import InlineModelAdmin


class InlineWeekAdmin(InlineModelAdmin):
    model = Week
    fields = ["week_id", "exercise_names"]
    readonly_fields = ["week_id", "exercise_names"]
    min_num = Week.MIN_COUNT
    max_num = Week.MAX_COUNT
    extra = 0

    def has_delete_permission(self, request, obj):
        return False
        return obj.weeks.all().count() > self.min_num

    def has_add_permission(self, request, obj):
        return False
        return obj.weeks.all().count() < self.max_num

    @admin.display(description="Exercises")
    def exercise_names(self, obj):
        return ""
        # exercises_qs = Exercise.objects.filter(week__pk=obj.pk)
        # return create_links_from_queryset(exercises_qs, label_field="name")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    model = Program
    inlines = (InlineWeekAdmin,)
    list_filter = ("profile",)
    # fields = ("profile", "name", "startdate", "duration", "order")
    fieldsets = (
        (
            _("Program Settings"),
            {"fields": ("profile", "name", "startdate", "duration", "order")},
        ),
    )
