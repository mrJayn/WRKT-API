import itertools
from rest_framework.routers import (
    SimpleRouter,
    Route,
    DynamicRoute,
    flatten,
    escape_curly_brackets,
)
from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path


class CustomRouter(SimpleRouter):
    """
    A `SimpleRouter` which provides an `formatted` kwarg which defaults to False.\n
        Setting `formatted` True, will remove the slash between the `prefix` and the `lookup`,\n and for plural actions "list" and "create", will append an "s" to the `prefix`.
    """

    routes = [
        Route(
            url=r"^{prefix}/$",
            mapping={
                "get": "list",
                "post": "create",
            },
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": ""},
        ),
        DynamicRoute(
            url=r"^{prefix}/{url_path}/$",
            name="{basename}-{url_name}",
            detail=False,
            initkwargs={},
        ),
        Route(
            url=r"^{prefix}{detail_separator}{lookup}/$",
            mapping={
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-update",
            detail=True,
            initkwargs={"suffix": "Update"},
        ),
        DynamicRoute(
            url=r"^{prefix}{detail_separator}{lookup}/{url_path}/$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={},
        ),
    ]

    def register(self, prefix, viewset, detail_separator=True, basename=None):
        if basename is None:
            basename = prefix.split("/")[-1].strip()
        detail_separator = "/" if detail_separator else ""
        self.registry.append((prefix, viewset, basename, detail_separator))
        # invalidate the urls cache
        if hasattr(self, "_urls"):
            del self._urls

    def get_urls(self):
        ret = []
        for prefix, viewset, basename, detail_separator in self.registry:
            lookup = self.get_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue
                # Build the url pattern
                regex = route.url.format(
                    prefix=prefix,
                    lookup=lookup,
                    detail_separator=detail_separator,
                )
                # Check for missing prefix.
                if not prefix and regex[:2] == "^/":
                    regex = "^" + regex[2:]

                initkwargs = route.initkwargs.copy()
                initkwargs.update({"basename": basename, "detail": route.detail})

                view = viewset.as_view(mapping, **initkwargs)
                name = route.name.format(basename=basename)
                ret.append(re_path(regex, view))  # name=name

        return ret


class SingleModelRouter(CustomRouter):
    routes = [
        Route(
            url=r"^{prefix}/$",
            mapping={
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=False,
            initkwargs={"suffix": "Detail"},
        ),
        Route(
            url=r"^{prefix}/add/$",
            mapping={"post": "create"},
            name="{basename}-create",
            detail=False,
            initkwargs={"suffix": "Create"},
        ),
    ]
