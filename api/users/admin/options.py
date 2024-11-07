from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest


class InlineModelAdmin(admin.TabularInline):
    extra = 0
    show_change_link = True
    filter_kwargs = None

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if self.filter_kwargs is not None:
            return qs.filter(**self.filter_kwargs)
        return qs

    def get_min_num(self, *args, **kwargs):
        return self.min_num or getattr(self.model, "MIN_COUNT", 0)

    def get_max_num(self, *args, **kwargs):
        return self.max_num or getattr(self.model, "MAX_COUNT", None)

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return self.get_queryset(request).count() > self.get_min_num()

    def has_add_permission(self, request, obj):
        max_count = self.get_max_num()
        return max_count and self.get_queryset(request).count() < max_count
