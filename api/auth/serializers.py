from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from api.users.models import CustomUser


class ValidateUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email", "phone_number"]

    def validate_phone_number(self, value):
        if value:
            queryset = self.Meta.model.objects.all()
            queryset = queryset.filter(phone_number__contains=value)
            if queryset.exists():
                raise ValidationError(
                    "This phone number is already being used.",
                    code="unique",
                )
        return value


class RegisterSerializer(ModelSerializer):
    # Creating the user, profile and library can be timely, so by creating all of them
    # before the end of the user serialization, their loading states can be grouped,
    # hence simplifying the client loading state and timing.

    class Meta:
        model = CustomUser
        fields = ["email", "password", "username"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        try:
            return self.Meta.model.objects.create_user(**validated_data)
        except TypeError:
            raise TypeError("Got an error while calling `CustomUser.create()`.")

    def to_representation(self, user):
        token = RefreshToken.for_user(user)
        return {
            "refresh": str(token),
            "access": str(token.access_token),
        }


class LoginSerializer(TokenObtainPairSerializer):
    username_field = "email"

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     # token["user_pk"] = user.pk
    #     return token
