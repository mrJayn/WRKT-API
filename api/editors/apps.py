from django.apps import AppConfig, apps
from django.db.models.signals import pre_save, post_delete


class EditorsConfig(AppConfig):
    name = "api.editors"
    label = "api_editors"

    def ready(self):
        from .models import EditorModel

        for cls in apps.get_models():
            if issubclass(cls, EditorModel):
                pre_save.connect(
                    cls._pre_editor_save, sender=cls, dispatch_uid=cls.__name__
                )
                post_delete.connect(
                    cls._on_editor_delete, sender=cls, dispatch_uid=cls.__name__
                )
