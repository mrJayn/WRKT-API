from utils.serializers import UserModelSerializer
from .models import User


class UserSerializer(UserModelSerializer):

    class Meta:
        model = User
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
