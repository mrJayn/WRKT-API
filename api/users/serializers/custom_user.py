from rest_framework import serializers
from utils.serializers import UserModelSerializer
from api.users.models import CustomUser, Profile


class ProfileSerializer(UserModelSerializer):
    """
    A ModelSerializer for model instances of the `Profile` model class.
    """

    class Meta:
        model = Profile
        fields = [
            "id",
            "notifications",
            "day_one_wkday",
            "units",
            "theme",
            "locale",
        ]


class CustomUserSerializer(UserModelSerializer):
    """
    A ModelSerializer for model instances of the `CustomUser` model class.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "last_login",
            "date_joined",
            # "password",
            # "inactive_start_date",
            # "is_staff",
            # "is_superuser",
            # "groups",
            # "user_permissions",
        ]
        read_only_fields = [
            "last_login",
            "date_joined",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to change the password of a user.
    """

    model = CustomUser

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
