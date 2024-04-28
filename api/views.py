from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import UserRateThrottle

from django.core.exceptions import ObjectDoesNotExist

from static.routes import ROUTES


class OncePerDayUserThrottle(UserRateThrottle):
    rate = "1/day"


class RoutesPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.get("url")[:5] == "/user":
            return bool(request.user and request.user.is_authenticated)
        return True


# ==========


class RoutesView(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get("name", None)
        if name:
            obj = ROUTES.get(name, None)
            if obj is None:
                raise ObjectDoesNotExist("Route does not exist.")
            return Response(obj)
        return Response(ROUTES)

    """
    # Good ✔️ - http://example.com/foobar/
    # Bad   ❌ - /foobar

    def get(self, request):
        year = now().year
        data = {
            "workout-list-url": reverse("year-summary", args=[year], request=request)
        }
        return Response(data)
    """
