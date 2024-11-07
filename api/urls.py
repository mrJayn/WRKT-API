from django.urls import path, include
from api.views import APIPingView, APIRoutesView

urlpatterns = [
    path(r"ping/", APIPingView.as_view(), name="ping"),
    path(r"routes/", APIRoutesView.as_view(), name="routes"),
    path(r"auth/", include("api.auth.urls")),
    path(r"", include("api.users.urls")),
]
