import re

from django.urls.resolvers import get_resolver

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.text import camel_case


class APIPingView(APIView):
    """View to test server reachability."""

    permission_classes = []

    def get(self, request):
        return Response(
            {
                "status": "online",
                "message": "Server is connected",
            },
            status=status.HTTP_200_OK,
        )


class APIRoutesView(APIView):
    """View to list all routes."""

    http_method_names = ["get", "head"]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        lookups = get_resolver().reverse_dict
        routes = {}

        for name in reversed(lookups.keys()):
            if isinstance(name, str):
                uri = lookups[name][0][0][0]
                uri = re.sub(r"\%\((?P<group>\w+)\)s", r":\g<group>", uri)
                uri = uri.removeprefix("api/").removesuffix("/")
                routes[camel_case(name)] = uri

        return Response(routes)
