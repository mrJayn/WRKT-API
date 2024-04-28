from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field import phonenumber

from django.core import validators
from django.utils.translation import gettext_lazy as _

from api.users.models import CustomUser, Profile, LibraryExercise


def is_valid_email_address(value):
    try:
        validators.validate_email(value)
        return True
    except ValidationError(_("Invalid email.")):
        return False


def is_valid_phone_number(value):
    phone_number = phonenumber.to_python(value)
    return phone_number and phone_number.is_valid()


"""
    email_or_phone = serializers.CharField(max_length=256)

    ###

    def validate(self, attrs):
        email_or_phone = attrs.pop("email_or_phone")

        if is_valid_email_address(email_or_phone):
            attrs["email"] = email_or_phone
        elif is_valid_phone_number(email_or_phone):
            attrs["phone_number"] = email_or_phone
        else:
            raise ValidationError(
                _("Enter either a valid email address or phone number.")
            )
        return attrs
"""

"""
    # day_one_wkday = serializers.IntegerField(default=0, min_value=0, max_value=6)
    # units = serializers.ChoiceField(default=Profile.Units.LBS, choices=Profile.Units, max_length=2)

    day_one_wkday = serializers.ModelField(
        model_field=Profile._meta.get_field("day_one_wkday"),
    )
    units = serializers.ModelField(
        model_field=Profile._meta.get_field("units"),
    )
"""


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "username",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        # Create the user's profile and library exercises.
        profile = Profile.objects.create(user=user)
        LibraryExercise.create_default_library(profile=profile)
        print("UserCreated!")
        return user

    def to_representation(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class ValidateRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email"]

    # def validate_phone_number(self, value):
    #     if value:
    #         queryset = self.Meta.model.objects.all()
    #         queryset = queryset.filter(phone_number__contains=value)

    #         if queryset.exists():
    #             raise ValidationError(
    #                 _("This phone number is already being used."), code="unique"
    #             )
    #     return value


class LoginSerializer(TokenObtainPairSerializer):
    username_field = "email"
