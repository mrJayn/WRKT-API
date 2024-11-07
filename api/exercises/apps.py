from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    name = "api.exercises"
    label = "api_exercises"
    verbose_name = "Exercise Library"

    # def ready(self):
    #     from .models import Exercise

    #     for cls in apps.get_models():
    #         if issubclass(cls, Exercise):
    #             post_save.connect(
    #                 cls._on_exercise_save, sender=cls, dispatch_uid=cls.__name__
    #             )
