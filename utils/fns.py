# from django.utils.translation import gettext_lazy as _
# from api.users import models


# def get_day_object(request, **kwargs):
#     """Return an `instance` of the `Day` model."""
#     if "wkt_order" not in kwargs:
#         return None
#     workout = request.user.profile.workouts.get(order=kwargs["wkt_order"])
#     return workout.days.get(day_id=kwargs["day_id"])


# def get_week_object(request, **kwargs):
#     """Return an `instance` of the `Week` model."""
#     if "prg_order" not in kwargs:
#         return None
#     program = request.user.profile.programs.get(order=kwargs["prg_order"])
#     return program.weeks.get(week_id=kwargs["week_id"])


# def query_exercise(request, **kwargs):
#     """Return a `queryset` or a model `instance` for 'Exercise'."""
#     wrt_map = {"day": None, "week": None}

#     if "workout" in request.path:
#         wrt_map["day"] = get_day_object(request, **kwargs)
#     elif "program" in request.path:
#         wrt_map["week"] = get_week_object(request, **kwargs)
#     else:
#         raise LookupError(
#             "Expected url path to contain the substring 'workout' or 'program'."
#         )

#     exercise_qs = models.Exercise.objects.filter(**wrt_map)

#     if "ex_order" in kwargs:
#         return exercise_qs.get(order=kwargs["ex_order"])
#     return exercise_qs
