from rest_framework_simplejwt.tokens import RefreshToken

# from django.conf import settings
# from django.contrib.auth.signals import ( user_logged_in, user_logged_out, user_login_failed )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
