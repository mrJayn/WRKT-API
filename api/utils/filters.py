from rest_framework import filters
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model, QuerySet, ForeignKey, Q


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """Filter that only allows users to see their own objects."""

    def filter_queryset(self, request, queryset, view):
        field_names = [
            field.name
            for field in queryset.model._meta.get_fields()
            if isinstance(field, ForeignKey)
        ]

        filter_kwargs = {}
        if "user" in field_names:
            filter_kwargs["user"] = request.user
        elif "profile" in field_names:
            filter_kwargs["profile"] = request.user.profile

        return queryset.filter(**filter_kwargs)


class CurrentUserFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        model_name = queryset.model._meta.model_name

        q = Q()
        if model_name == "exercise":
            q.add(Q(day__workout__profile__user=request.user))
            q.add(Q(week__program__profile__user=request.user), Q.OR)
        elif model_name == "day":
            q.add(Q(workout__profile__user=request.user))
        elif model_name == "week":
            q.add(Q(program__profile__user=request.user))
        else:
            return queryset
        return queryset.filter(q)
