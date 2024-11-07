from django.apps import apps
from django.conf import settings as django_settings

############################
#           MOVE TO SETTINGS            #
############################

# ( Required ) URL of the frontend "password-reset" page.
PASSWORD_RESET_CONFIRM_URL = ""

# ( Required ) URL of the frontend "username-reset" page.
USERNAME_RESET_CONFIRM_URL = ""

# ( Required ) URL of the frontend "activation" page.
ACTIVATION_URL = ""


# NOTE:
# Each URL should contain { uid } and { token } placeholders,
# e.g. #/password-reset/{uid}/{token}.

############################
#           MOVE TO SETTINGS            #
############################


auth_module, user_model = django_settings.AUTH_USER_MODEL.rsplit(".", 1)
User = apps.get_model(auth_module, user_model)


# Field name of the ID field for the user.
USER_ID_FIELD = User._meta.pk.name

# Field name of the credential used to login in user.
LOGIN_FIELD = User.USERNAME_FIELD

# Replaces the DOMAIN part of the url in the emails content.
EMAIL_FRONTEND_DOMAIN = None

# Replaces the PROTOCOL part of the url in the emails content.
EMAIL_FRONTEND_PROTOCOL = None

# Replaces the SITE_NAME in the emails content.
EMAIL_FRONTEND_SITE_NAME = None

# Send an email to the user to activate their account.
SEND_ACTIVATION_EMAIL = False

# Send an email to the user to verify their email.
SEND_CONFIRMATION_EMAIL = False

# If True, "change-password" endpoints will send a confirmation email to user.
PASSWORD_CHANGED_EMAIL_CONFIRMATION = False

# If True, "change-username" endpoints will send confirmation email to user.
USERNAME_CHANGED_EMAIL_CONFIRMATION = False

# If True, you need to pass "re_password" to `/users/ endpoint`, to validate password equality.
USER_CREATE_PASSWORD_RETYPE = False

# If True, you need to pass "re_new_username" to `/users/set_username/` endpoint, to validate username equality.
SET_USERNAME_RETYPE = False

# If True, you need to pass "re_new_password" to `/users/set_password/` endpoint, to validate password equality.
SET_PASSWORD_RETYPE = False

# If True, you need to pass "re_new_password" to `/users/reset_password_confirm/` endpoint, to validate password equality.
PASSWORD_RESET_CONFIRM_RETYPE = False

# If True, you need to pass "re_new_username" to `/users/reset_username_confirm/` endpoint, to validate username equality.
USERNAME_RESET_CONFIRM_RETYPE = False

# If True, setting new password will logout the user.
LOGOUT_ON_PASSWORD_CHANGE = False

# If True, posting a non-existent email to the `/users/reset_password/` endpoint
# will return a `HTTP_400_BAD_REQUEST` response with an `EMAIL_NOT_FOUND` error message.
# otherwise, will return a `HTTP_204_NO_CONTENT` response.
PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND = False

# If True, posting a non-existent email to the `/users/reset_username/` endpoint
# will return a `HTTP_400_BAD_REQUEST` response with an `EMAIL_NOT_FOUND` error message.
# otherwise, will return a `HTTP_204_NO_CONTENT` response.
USERNAME_RESET_SHOW_EMAIL_NOT_FOUND = False

# Token model used for authentication.
TOKEN_MODEL = "rest_framework.authtoken.models.Token"

# Permission Classes
PERMISSIONS = {
    "activation": ["rest_framework.permissions.AllowAny"],
    "password_reset": ["rest_framework.permissions.AllowAny"],
    "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
    "set_password": ["api.utils.permissions.IsCurrentUserOrAdmin"],
    "username_reset": ["rest_framework.permissions.AllowAny"],
    "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
    "set_username": ["api.utils.permissions.IsCurrentUserOrAdmin"],
    "user_create": ["rest_framework.permissions.AllowAny"],
    "user_delete": ["api.utils.permissions.IsCurrentUserOrAdmin"],
    "user": ["api.utils.permissions.IsCurrentUserOrAdmin"],
    "user_list": ["api.utils.permissions.IsCurrentUserOrAdmin"],
    "token_create": ["rest_framework.permissions.AllowAny"],
    "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
}

# ⚠️⚠️⚠️⚠️
# Serializer Classes
_SERIALIZERS = {
    "activation": "api.user.serializers.ActivationSerializer",
    "password_reset": "api.user.serializers.SendEmailResetSerializer",
    "password_reset_confirm": "api.user.serializers.PasswordResetConfirmSerializer",
    "password_reset_confirm_retype": "api.user.serializers.PasswordResetConfirmRetypeSerializer",
    "set_password": "api.user.serializers.SetPasswordSerializer",
    "set_password_retype": "api.user.serializers.SetPasswordRetypeSerializer",
    "set_username": "api.user.serializers.SetUsernameSerializer",
    "set_username_retype": "api.user.serializers.SetUsernameRetypeSerializer",
    "username_reset": "api.user.serializers.SendEmailResetSerializer",
    "username_reset_confirm": "api.user.serializers.UsernameResetConfirmSerializer",
    "username_reset_confirm_retype": "api.user.serializers.UsernameResetConfirmRetypeSerializer",
    "user": "api.user.serializers.UserSerializer",
    "user_create": "api.user.serializers.UserCreateSerializer",
    "user_create_password_retype": "api.user.serializers.UserCreatePasswordRetypeSerializer",
    "user_delete": "api.user.serializers.UserDeleteSerializer",
    "current_user": "api.user.serializers.UserSerializer",
    "token": "api.user.serializers.TokenSerializer",
    "token_create": "api.user.serializers.TokenCreateSerializer",
}


# ⚠️⚠️⚠️⚠️
# Email Classes
_EMAIL = {
    "activation": "djoser.email.ActivationEmail",
    "confirmation": "djoser.email.ConfirmationEmail",
    "password_reset": "djoser.email.PasswordResetEmail",
    "password_changed_confirmation": "djoser.email.PasswordChangedConfirmationEmail",
    "username_changed_confirmation": "djoser.email.UsernameChangedConfirmationEmail",
    "username_reset": "djoser.email.UsernameResetEmail",
}

# Constant Classes
CONSTANTS = {"messages": "api.user.constants.Messages"}


# Sessions
CREATE_SESSION_ON_LOGIN = False


# ⚠️⚠️⚠️⚠️
# Path to class responsible for token strategy used by social authentication.
SOCIAL_AUTH_TOKEN_STRATEGY = None  # "djoser.social.token.jwt.TokenStrategy"


# List of allowed redirect URIs for social authentication.
SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = []


# If True, the  `/users/` enpoint by a non-admin user will return only the instance of that user.
# Beside that, accessing `/users/<id>/` endpoints by user without proper permission will result in HTTP 404 instead of HTTP 403.
HIDE_USERS = True


#########################
#          Custom Attributes          #
#########################

USER_DIR = "api.user"
CONSTANTS_DIR = "api.user.constants"

#  Serializers
ACTIVATION_SERIALIZER = "api.user.serializers.ActivationSerializer"
SET_PASSWORD_SERIALIZER = "api.user.serializers.SetPasswordSerializer"
SET_PASSWORD_RETYPE_SERIALIZER = "api.user.serializers.SetPasswordRetypeSerializer"
PASSWORD_RESET_SERIALIZER = "api.user.serializers.SendEmailResetSerializer"
PASSWORD_RESET_CONFIRM_SERIALIZER = (
    "api.user.serializers.PasswordResetConfirmSerializer"
)
PASSWORD_RESET_CONFIRM_RETYPE_SERIALIZER = (
    "api.user.serializers.PasswordResetConfirmRetypeSerializer"
)
SET_USERNAME_SERIALIZER = "api.user.serializers.SetUsernameSerializer"
SET_USERNAME_RETYPE_SERIALIZER = "api.user.serializers.SetUsernameRetypeSerializer"
USERNAME_RESET_SERIALIZER = "api.user.serializers.SendEmailResetSerializer"
USERNAME_RESET_CONFIRM_SERIALIZER = (
    "api.user.serializers.UsernameResetConfirmSerializer"
)
USERNAME_RESET_CONFIRM_RETYPE_SERIALIZER = (
    "api.user.serializers.UsernameResetConfirmRetypeSerializer"
)
USER_SERIALIZER = "api.user.serializers.UserSerializer"
USER_CREATE_SERIALIZER = "api.user.serializers.UserCreateSerializer"
USER_CREATE_PASSWORD_RETYPE_SERIALIZER = (
    "api.user.serializers.UserCreatePasswordRetypeSerializer"
)
USER_DELETE_SERIALIZER = "api.user.serializers.UserDeleteSerializer"
CURRENT_USER_SERIALIZER = "api.user.serializers.UserSerializer"
TOKEN_SERIALIZER = "api.user.serializers.TokenSerializer"
TOKEN_CREATE_SERIALIZER = "api.user.serializers.TokenCreateSerializer"


"""
_default_settings = {
    "USER_ID_FIELD": User._meta.pk.name,
    "LOGIN_FIELD": User.USERNAME_FIELD,
    "SEND_ACTIVATION_EMAIL": False,
    "SEND_CONFIRMATION_EMAIL": False,
    "USER_CREATE_PASSWORD_RETYPE": False,
    "SET_PASSWORD_RETYPE": False,
    "PASSWORD_RESET_CONFIRM_RETYPE": False,
    "SET_USERNAME_RETYPE": False,
    "USERNAME_RESET_CONFIRM_RETYPE": False,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": False,
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",
    "SERIALIZERS": {
            "activation": "djoser.serializers.ActivationSerializer",
            "password_reset": "djoser.serializers.SendEmailResetSerializer",
            "password_reset_confirm": "djoser.serializers.PasswordResetConfirmSerializer",
            "password_reset_confirm_retype": "djoser.serializers.PasswordResetConfirmRetypeSerializer",
            "set_password": "djoser.serializers.SetPasswordSerializer",
            "set_password_retype": "djoser.serializers.SetPasswordRetypeSerializer",
            "set_username": "djoser.serializers.SetUsernameSerializer",
            "set_username_retype": "djoser.serializers.SetUsernameRetypeSerializer",
            "username_reset": "djoser.serializers.SendEmailResetSerializer",
            "username_reset_confirm": "djoser.serializers.UsernameResetConfirmSerializer",
            "username_reset_confirm_retype": "djoser.serializers.UsernameResetConfirmRetypeSerializer",
            "user_create": "djoser.serializers.UserCreateSerializer",
            "user_create_password_retype": "djoser.serializers.UserCreatePasswordRetypeSerializer",
            "user_delete": "djoser.serializers.UserDeleteSerializer",
            "user": "djoser.serializers.UserSerializer",
            "current_user": "djoser.serializers.UserSerializer",
            "token": "djoser.serializers.TokenSerializer",
            "token_create": "djoser.serializers.TokenCreateSerializer",
        },
    "EMAIL": {
            "activation": "djoser.email.ActivationEmail",
            "confirmation": "djoser.email.ConfirmationEmail",
            "password_reset": "djoser.email.PasswordResetEmail",
            "password_changed_confirmation": "djoser.email.PasswordChangedConfirmationEmail",
            "username_changed_confirmation": "djoser.email.UsernameChangedConfirmationEmail",
            "username_reset": "djoser.email.UsernameResetEmail",
        },
    "EMAIL_FRONTEND_DOMAIN": None,
    "EMAIL_FRONTEND_PROTOCOL": None,
    "EMAIL_FRONTEND_SITE_NAME": None,
    "CONSTANTS": {"messages": "api.constants.Messages"},
    "LOGOUT_ON_PASSWORD_CHANGE": False,
    "CREATE_SESSION_ON_LOGIN": False,
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [],
    "HIDE_USERS": True,
    "PERMISSIONS": {
            "activation": ["rest_framework.permissions.AllowAny"],
            "password_reset": ["rest_framework.permissions.AllowAny"],
            "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_password": ["api.utils.permissions.IsCurrentUserOrAdmin"],
            "username_reset": ["rest_framework.permissions.AllowAny"],
            "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_username": ["api.utils.permissions.IsCurrentUserOrAdmin"],
            "user_create": ["rest_framework.permissions.AllowAny"],
            "user_delete": ["api.utils.permissions.IsCurrentUserOrAdmin"],
            "user": ["api.utils.permissions.IsCurrentUserOrAdmin"],
            "user_list": ["api.utils.permissions.IsCurrentUserOrAdmin"],
            "token_create": ["rest_framework.permissions.AllowAny"],
            "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
        },
    "WEBAUTHN": {
            "RP_NAME": "localhost",
            "RP_ID": "localhost",
            "ORIGIN": "http://localhost:8000",
            "CHALLENGE_LENGTH": 32,
            "UKEY_LENGTH": 20,
            "SIGNUP_SERIALIZER": "djoser.webauthn.serializers.WebauthnCreateUserSerializer",
            "LOGIN_SERIALIZER": "djoser.webauthn.serializers.WebauthnLoginSerializer",
        },
}
"""
