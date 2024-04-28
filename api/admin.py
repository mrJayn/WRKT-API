from string import Template

from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse

from django.utils import timezone, safestring
from django.utils.translation import gettext_lazy as _

from api.users import models
from api.users.models import CustomUser


def get_filter_str(obj):
    filter_strs = ["{}={}".format(k, v) for k, v in obj.items()]
    return ",".join(filter_strs)


def admin_change_view_link(view_base, args=None, params=None):
    view_suffix, search_params = (
        ("changelist", "".join(["?", get_filter_str(params)]))
        if params and isinstance(params, object)
        else ("change", "")
    )
    url = reverse(
        "admin:api_users_{}_{}".format(view_base, view_suffix),
        args=args,
    )
    return safestring.mark_safe(
        _('<a href="{url}{search_params}">{label}</a>').format(
            url=url,
            search_params=search_params,
            label=view_base.capitalize(),
        )
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    fieldsets = (
        (None, {"fields": ("profile_link",)}),
        (_("Account"), {"fields": ("username", "email", "phone_number", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name")}),
        (_("Dates"), {"fields": ("date_joined", "last_login")}),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_superuser", "user_permissions")},
        ),
        (_("Active Status"), {"fields": ("is_active",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2"),
            },
        ),
    )
    # form
    # add_form
    # change_password_form
    list_display = (
        "__str__",
        "email",
        "phone_number",
        "is_active",
        "is_superuser",
    )
    list_filter = ("is_active", "is_superuser")
    search_fields = ("email", "phone_number")
    ordering = ("id",)
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("profile_link", "last_login", "date_joined")

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)

        if obj is not None and not obj.is_active:
            #  display time until delete for inactive users.
            form.base_fields["is_active"].help_text += self.inactive_help_text(obj)

        if not request.user.is_superuser:
            # only superusers can edit permissions.
            form.base_fields["is_superuser"].disabled = True
        return form

    def inactive_help_text(self, obj):
        lifespan = timezone.timedelta(days=settings.INACTIVE_USER_LIFESPAN_DAYS)
        td = (obj.inactive_start_date + lifespan) - timezone.now()
        return _(
            '<br/>⚠️<span style="color: #ffbd57;"> Delete in: '
            "[ {d:02} days : {h:02} hours : {m:02} minutes ]</span>"
        ).format(
            d=int(td.days),
            h=int(td.seconds // 3600),
            m=int((td.seconds // 60) % 60),
        )

    @admin.display(description="View Profile")
    def profile_link(self, obj):
        return admin_change_view_link("profile", args=(obj.profile.id,))


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = models.Profile
    fieldsets = (
        (None, {"fields": ("user_link", "library_link")}),
        (_("Profile"), {"fields": ("notifications", "day_one_wkday", "units")}),
    )
    readonly_fields = ("user_link", "library_link")
    actions = None

    @admin.display(description="Account")
    def user_link(self, obj):
        return admin_change_view_link("customuser", args=(obj.user.pk,))

    @admin.display(description="Library")
    def library_link(self, obj):
        return admin_change_view_link(
            "libraryexercise",
            params={"profile__id__exact": obj.id},
        )


class Inline_Day(admin.TabularInline):
    model = models.Day
    fields = ["day_id", "name"]
    readonly_fields = ["day_id"]
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


@admin.register(models.Workout)
class WorkoutAdmin(admin.ModelAdmin):
    model = models.Workout
    inlines = (Inline_Day,)
    list_filter = ("profile",)
    fieldsets = ((_("Workout Settings"), {"fields": ("name", "is_active", "order")}),)


# =============
#   Program


class Inline_ProgramWeek(admin.TabularInline):
    model = models.Week
    fields = ["week_id", "ex_list"]
    readonly_fields = ["week_id", "ex_list"]
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    @admin.display(description="Exercises")
    def ex_list(self, obj):
        prog_week_exs = models.Exercise.objects.programs(week=obj.pk)
        names = list(prog_week_exs.values_list("name", flat=True))

        def get_name(index, default="-"):
            try:
                name = names[index]
                return default if not name else name
            except IndexError:
                return default

        template_str = Template("{} $sp {} $sp {}").safe_substitute(sp="\u00A0/\u00A0")
        return template_str.format(get_name(0), get_name(1), get_name(2))


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    model = models.Program
    inlines = (Inline_ProgramWeek,)
    list_filter = ("profile",)
    # fields = ("profile", "name", "startdate", "duration", "order")
    fieldsets = (
        (_("Program Settings"), {"fields": ("name", "startdate", "duration", "order")}),
    )


#   Exercise + SecondaryExercise + Set
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


class Inline_SecondaryExercise(admin.TabularInline):
    model = models.SecondaryExercise


class Inline_ExerciseSets(admin.TabularInline):
    model = models.ExerciseSet
    max_num = 3

    # def has_delete_permission(self, request, obj):
    #     return obj.day is not None

    # def get_fields(self, request, obj):
    #     if obj.day is None:
    #         return ["order", "sets", "reps", "percent"]
    #     if obj.week is None:
    #         return ["order", "sets", "reps", "weight"]

    # def get_readonly_fields(self, request, obj):
    #     if obj.day is None:
    #         return ["order"]


@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    inlines = [Inline_SecondaryExercise, Inline_ExerciseSets]
    model = models.Exercise
    fields = ["day", "week", "name", "order"]
    # list_filter = [ParentListFilter]

    # def get_fields(self, request, obj):
    #     fields = list(super().get_fields(request, obj=obj))
    #     if obj.day is None:
    #         fields.remove("day")
    #         fields.remove("order")
    #     if obj.week is None:
    #         fields.remove("week")
    #     return fields


# ---------


@admin.register(models.LibraryExercise)
class LibraryExerciseAdmin(admin.ModelAdmin):
    model = models.LibraryExercise
    fields = ["profile", "name", "bodypart", "equipment", "enabled", "custom"]
    # readonly_fields = ["profile", "custom"]
    list_filter = ["profile", "custom"]
