from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
    token_verify,
    token_blacklist,
)
from django.urls import path
from .views import RegisterView, ValidateRegisterView

urlpatterns = [
    path(r"register/", RegisterView.as_view(), name="signup"),
    path(r"register/validate/", ValidateRegisterView.as_view(), name="validate-signup"),
    path(r"login/", token_obtain_pair, name="token-obtain-pair"),
    path(r"logout/", token_blacklist, name="token-blacklist"),
    path(r"refresh/", token_refresh, name="token-refresh"),
    path(r"verify/", token_verify, name="token-verify"),
    #
]
