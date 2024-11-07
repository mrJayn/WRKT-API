from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.validators import validate_email

from django.shortcuts import get_object_or_404
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _

from rest_framework import mixins, permissions, status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from utils.mixins import PartialUpdateModelMixin

from api.users.models import CustomUser
from api.users.serializers.custom_user import (
    CustomUserSerializer,
    ChangePasswordSerializer,
)
from api.utils.permissions import IsCurrentUserOrAdmin

""" CustomUser Views

Safe Views
 * retrieve
 * partial_update ( email, phone_number, username, first_name, last_name, is_active )

Auth Views
 * create
 * destroy

"""


METHODS_MAP = {
    "get": "retrieve",
    "patch": "partial_update",
    "delete": "destroy",
    # "post": "create",
}

_SAFE_FIELDS = (
    "username",
    "email",
    "phone_number",
    "first_name",
    "last_name",
    "is_active",
)


class CustomUserViewSet(
    mixins.RetrieveModelMixin,
    PartialUpdateModelMixin,
    GenericViewSet,
):
    """
    Viewset to retrieve and partially-update the `CustomUser` model instance for the current user.
    """

    http_method_names = ["get", "patch", "destroy"]
    # queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsCurrentUserOrAdmin]

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj

    @classonlymethod
    def as_detail_view(self):
        return self.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
            }
        )

    @classonlymethod
    def as_readonly_view(self):
        return self.as_view({"get": "retrieve"})

    @classonlymethod
    def as_partial_update_view(self):
        return self.as_view({"get": "retrieve"})

    @classonlymethod
    def as_destroy_view(self):
        return self.as_view({"get": "retrieve"})

    @classonlymethod
    def _as_view(self, method):
        if method not in self.http_method_names:
            raise ImproperlyConfigured(
                "'%s' is not a method for the `CustomUserViewSet`." % method
            )
        actions = {method: METHODS_MAP[method]}
        return self.as_view(actions)


# ========== ========== ==========


class CustomUserReadOnlyView(RetrieveAPIView):
    """Retrieve the `CustomUser` model instance for the current user."""

    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class _UserChangePasswordView(UpdateAPIView):
    """Change the password for the current user."""

    model = CustomUser
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        self.object = user
        # request.data = { "old_password":str, "new_password":str }
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password

        if not user.check_password(serializer.data["old_password"]):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # set_password also hashes the password that the user will get
        self.object.set_password(serializer.data["new_password"])
        self.object.save()

        return Response(
            {"message": "Password updated successfully!"},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    """Change the password for the current user."""

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        validate_email(email)

        try:
            send_mail(
                subject=_("Wrkt App - Reset Password"),
                message=_("Use this link to reset your password."),
                from_email=_("m63jayne@gmail.com"),
                recipient_list=[email],
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
