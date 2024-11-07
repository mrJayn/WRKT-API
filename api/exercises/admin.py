from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BaseExercise


@admin.register(BaseExercise)
class BaseExerciseAdmin(admin.ModelAdmin):
    fields = ["name", "bodypart", "equipment"]
    list_filter = ["bodypart", "equipment"]
    search_fields = ["name"]
