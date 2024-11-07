from django.utils.translation import gettext_lazy as _
from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from rest_framework.viewsets import ModelViewSet

from itertools import filterfalse, tee


def partition(pred, iterable):
    """Use a predicate to partition entries into false entries and true entries"""
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


LIST_ROUTE = Route(
    url=r"{prefix}/$",
    mapping={
        "get": "list",
        "post": "create",
    },
    name="{basename}s-list",
    detail=False,
    initkwargs={"suffix": "List"},
)

DETAIL_ROUTE = Route(
    url=r"{prefix}/{lookup}/$",
    mapping={
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    },
    name="{basename}-detail",
    detail=True,
    initkwargs={"suffix": "Detail"},
)

DYNAMIC_LIST_ROUTE = DynamicRoute(
    url=r"{prefix}/{url_path}/$",
    name="{basename}s-{url_name}",
    detail=False,
    initkwargs={},
)

DYNAMIC_DETAIL_ROUTE = DynamicRoute(
    url=r"{prefix}/{lookup}/{url_path}/$",
    name="{basename}-{url_name}",
    detail=True,
    initkwargs={},
)


class APIRouter(SimpleRouter):
    routes = [
        LIST_ROUTE,
        DYNAMIC_LIST_ROUTE,
        DETAIL_ROUTE,
        DYNAMIC_DETAIL_ROUTE,
    ]

    def register(self, prefix, viewset, name=None):
        if name is None:
            name = prefix.split("/")[-1].strip().removesuffix("s")
        return super().register(prefix, viewset, name)


class NestedRouter(SimpleRouter):
    routes = [
        LIST_ROUTE,
        DETAIL_ROUTE,
    ]

    def register(self, *routes: tuple[str, ModelViewSet]):
        """
        Register multiple routes, each as a tuple containing `prefix`,`viewset`, and `basename`.

        For each route provided, the `prefix` will be preceeded by the prefix of the previous route,
        and the first route provided is conidered the "base".
        """
        acc_prefix = ""

        for name, viewset in routes:
            prefix = acc_prefix + name
            self.registry.append((prefix, viewset, name))

            # Get the accumulated prefix for the route.
            lookup = self.get_lookup_regex(
                viewset,
                lookup_prefix=name.removesuffix("s") + "_",
            )
            acc_prefix = "%s/%s/" % (prefix, lookup)


'''
    A `SimpleRouter` that provides a custom `.register()` method and `routes` attribute.

    { RouteTuple } - tuple[str, ModelViewSet]

    **Usage:**
    ``` py
    api_router = ApiRouter()
    # To register a single route:
    >> .register( "foobar", FoobarModelViewset )
    # To register multiple nested routes:
    >> .register(("foo", FooViewSet ), ( "bar", BarViewSet ), ...)
    """
    Resulting URL Patterns:
      1. "...foobars/" [ name="foobars-list"]
      2. "...foobars/<pk>/" [ name="foobar-detail"]
      3. "...foos/" [ name="foos-list"]
      4. "...foos/<pk>/" [ name="foo-detail"]
      5. "...foos/<foo_pk>/bars/" [ name="bars-list"]
      6. "...foos/<foo_pk>/bars/<pk>/" [ name="bar-detail"]
    """
    ```
'''
