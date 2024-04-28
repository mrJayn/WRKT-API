from django.db.models import Model
from django.http import QueryDict
from django.utils.translation import gettext_lazy as _

from api.users import models


def get_day_object(request, **kwargs):
    """Return an `instance` of the `Day` model."""
    if "wkt_order" not in kwargs:
        return None
    workout = request.user.profile.workouts.get(order=kwargs["wkt_order"])
    return workout.days.get(day_id=kwargs["day_id"])


def get_week_object(request, **kwargs):
    """Return an `instance` of the `Week` model."""
    if "prg_order" not in kwargs:
        return None
    program = request.user.profile.programs.get(order=kwargs["prg_order"])
    return program.weeks.get(week_id=kwargs["week_id"])


def query_exercise(request, **kwargs):
    """Return a `queryset` or a model `instance` for 'Exercise'."""
    wrt_map = {"day": None, "week": None}
    if "workout" in request.path:
        wrt_map["day"] = get_day_object(request, **kwargs)
    elif "program" in request.path:
        wrt_map["week"] = get_week_object(request, **kwargs)
    else:
        raise LookupError(
            "Expected url path to contain the substring 'workout' or 'program'."
        )
    exercise_qs = models.Exercise.objects.filter(**wrt_map)
    if "ex_order" in kwargs:
        return exercise_qs.get(order=kwargs["ex_order"])
    return exercise_qs


def get_user_from_ref(ref):
    """
    Returns a User instance from the given `ref` which must
    be an instance of a model class defined in 'api__users'.
    """
    if not isinstance(ref, Model):
        raise ValueError(_("`{}` is not a valid model instance.").format(ref))

    if isinstance(ref, models.Workout) or isinstance(ref, models.Program):
        return ref.profile.user
    elif isinstance(ref, models.Day):
        return ref.workout.profile.user
    elif isinstance(ref, models.Week):
        return ref.program.profile.user
    elif isinstance(ref, models.Exercise):
        pass
    elif isinstance(ref, models.SecondaryExercise) or isinstance(
        ref, models.ExerciseSet
    ):
        ref = ref.exercise
    else:
        return None

    if ref.day is not None:
        return ref.day.workout.profile.user
    if ref.week is not None:
        return ref.week.program.profile.user


def update_data(request, obj, clean=True):
    """Updates and cleans a `POST` request.data object."""
    if isinstance(request.data, QueryDict):
        request.data._mutable = True
    for k, v in obj.items():
        if v is not None:
            request.data[k] = obj[k]
    # remove the items with null value
    if clean:
        for k, v in request.data.copy().items():
            if v is None or v == "":
                del request.data[k]
    return request


def get_lookup_url_kwarg(modelName: str):
    modelName = modelName.lower()
    lookup_url_kwarg = None

    if modelName in ["workout", "program"]:
        lookup_url_kwarg = "aid"
    elif modelName in ["day", "week"]:
        lookup_url_kwarg = "bid"
    elif modelName in ["exercise"]:
        lookup_url_kwarg = "cid"
    elif modelName in ["secondary", "set"]:
        lookup_url_kwarg = "did"

    return lookup_url_kwarg
