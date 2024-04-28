from django.contrib import admin
from django.urls import path, include
from api.views import RoutesView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"", include("api.authentication.urls")),
    path(r"user/", include("api.users.urls")),
    path(r"routes/", RoutesView.as_view()),
    path(r"routes/<str:name>/", RoutesView.as_view()),
]
