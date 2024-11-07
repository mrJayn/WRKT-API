from string import Template
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model, ForeignKey, QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


def model_reverse(model: Model, args=None, query=None):
    _opts = model._meta
    info = (
        admin.site.name,
        _opts.app_label,
        _opts.model_name,
        ("list" if query else ""),
    )
    url = reverse("{}:{}_{}_change{}".format(*info), args=args)
    # If query kwargs are provided, then prepare
    # and encode them into a url query string.
    if query:
        query_strs = []
        for param, value in query.items():
            try:
                if isinstance(_opts.get_field(param), ForeignKey):
                    param += "__id"
            except FieldDoesNotExist:
                pass
            if isinstance(value, bool):
                value = 1 if value is True else 0
            query_strs.append("{}__exact={}".format(param, value))

        url = "{}?{}".format(url, "&".join(query_strs))

    return url


def linkto(ModelClass, args=None, params=None, label=None):
    url = model_reverse(ModelClass, args, params)

    return mark_safe(
        _('<a href="{url}">{label}</a>').format(
            url=url,
            label=label or ModelClass.__name__,
        )
    )


def create_links_from_queryset(queryset, label_field="name"):
    if not isinstance(queryset, QuerySet) or not queryset.exists():
        return mark_safe('<span style="color:#888;font-style:italic;">None</span>')

    ModelClass = queryset.model
    try:
        ModelClass._meta.get_field(label_field)
    except FieldDoesNotExist:
        raise ValueError(
            "label_field must be a field of the {} model.", ModelClass.__name__
        )

    items_list = list(queryset.values("id", label_field))
    link_els = []

    for i, item in enumerate(items_list):
        base = _(
            '<a class="button" href="{href}" style="padding: 3px 12px; margin-right: 5px; border-radius: 15px;">{text}</a>'
        )
        change_url = "admin:api_users_%s_change" % ModelClass._meta.model_name
        href = reverse(change_url, args=(item["id"],))
        name = item[label_field] or "%s %d" % (ModelClass.__name__, i + 1)
        link_els.append(
            base.format(
                href=href,
                text=name,
            )
        )

    return mark_safe("".join(link_els))
