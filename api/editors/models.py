from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from utils.models import OrderedModel
from utils.managers import OrderedModelQuerySet

from api.utils.helpers import did_field_change


class EditorModelQuerySet(OrderedModelQuerySet):
    def update_active(self, ref):
        if not did_field_change(ref, "is_active"):
            qs = self.exclude(pk=ref.pk)
            if ref.is_active:
                return qs.deactivate_all()
            return qs.activate_next()

    def deactivate_all(self):
        if self.exists() and self.filter(is_active=True).exists():
            return self.update(is_active=False)

    def activate_next(self):
        if self.exists():
            pk = self.first().pk
            self.filter(pk=pk).update(is_active=True)
            return self.exclude(pk=pk).deactivate_all()


class EditorModelManager(models.Manager.from_queryset(EditorModelQuerySet)):
    pass


class EditorModel(OrderedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        _("name"),
        max_length=50,
    )
    is_active = models.BooleanField(_("active"), default=False)

    objects = EditorModelManager()

    MIN_COUNT = 0
    MAX_COUNT = 3

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name").desc(), "user", name="unique_lower_name_user"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.get_default_name()
        return super().save(*args, **kwargs)

    def get_default_name(self):
        s = "New %s" % self.__class__.__name__
        qs = self.get_ordered_queryset()
        names = list(qs.values_list("name", flat=True))
        if s in names:
            tmp, n = "", 1
            while not tmp or tmp in names:
                tmp = s + " (%d)" % n
                n += 1
            s = tmp
        return s

    @classmethod
    def _pre_editor_save(cls, sender=None, instance=None, **kwargs):
        """Ensure one instance is active per ordered queryset."""
        ordered_qs = instance.get_ordered_queryset()
        if instance.pk:
            ordered_qs.update_active(instance)
        elif not ordered_qs.exists():
            setattr(instance, "is_active", True)

    @classmethod
    def _on_editor_delete(cls, sender=None, instance=None, **kwargs):
        """If deleted instance is active, then activate the next obj in the ordered queryset. ( if it exists )"""
        if instance.is_active:
            instance.get_ordered_queryset().activate_next()

    @property
    def breadcrumbs(self):
        return "{} - {}".format(self.user.__str__(), self.name)


class EditorItem(OrderedModel):
    editor = models.ForeignKey(
        EditorModel,
        on_delete=models.CASCADE,
        related_name="items",
    )
