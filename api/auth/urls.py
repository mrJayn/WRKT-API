from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_blacklist,
    token_refresh,
    token_verify,
)
from api.auth.views import RegisterView, ValidateUserView

urlpatterns = [
    path(r"register/", RegisterView.as_view(), name="register"),
    path(r"validate-unique/", ValidateUserView.as_view(), name="validate-user"),
    path(r"login/", token_obtain_pair, name="login"),
    path(r"logout/", token_blacklist, name="logout"),
    path(r"refresh/", token_refresh, name="refresh"),
    path(r"verify/", token_verify, name="verify"),
]
